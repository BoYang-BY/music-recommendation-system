import os
import glob
import math

from sqlmodel import (
    Session,
    create_engine
)

from sqlalchemy.dialects.postgresql import insert


from model import (
    Artist,
    Song,
    AudioFeatures,
    create_session,
    create_table,
    drop_table
)


import utils.hdf5_getters as hdf5_getters
from utils.extract_utils import extract_h5_info

def sanitize_value(value):
    """
    如果資料是 NaN 或 None，
    統一轉成 None
    """

    if value is None:
        return None

    if isinstance(value, float) and math.isnan(value):
        return None

    return value

def insert_song_data_bulk_mappings(
    session: Session,
    h5_data_list: list
):

    try:

        # =========================
        # 1. 建立 Artist 資料
        # =========================

        artist_mappings = [
            {
                "artist_id": sanitize_value(
                    artist_info["artist_id"]
                ),

                "artist_name": sanitize_value(
                    artist_info["artist_name"]
                ),

                "artist_hotness": sanitize_value(
                    artist_info["artist_hotness"]
                )
            }

            for artist_info in h5_data_list
        ]


        # 插入 Artist
        # 如果 artist_id 已存在則跳過

        stmt = insert(Artist).values(
            artist_mappings
        )

        stmt = stmt.on_conflict_do_nothing(
            index_elements=["artist_id"]
        )

        session.exec(stmt)



        # =========================
        # 2. 建立 Song 資料
        # =========================

        song_mappings = [

            {
                "song_id": sanitize_value(
                    song_info["song_id"]
                ),

                "artist_id": sanitize_value(
                    song_info["artist_id"]
                ),

                "song_title": sanitize_value(
                    song_info["song_title"]
                ),

                "song_hotness": sanitize_value(
                    song_info["song_hotness"]
                ),

                "year": sanitize_value(
                    song_info["year"]
                )
            }

            for song_info in h5_data_list

        ]


        # 批量寫入 Song

        session.bulk_insert_mappings(
            Song,
            song_mappings
        )



        # =========================
        # 3. 建立 AudioFeatures 資料
        # =========================

        audio_features_mappings = [

            {

                "song_id": sanitize_value(
                    song_info["song_id"]
                ),

                "danceability": sanitize_value(
                    song_info["audio_features"]["danceability"]
                ),

                "energy": sanitize_value(
                    song_info["audio_features"]["energy"]
                ),

                "key": sanitize_value(
                    song_info["audio_features"]["key"]
                ),

                "loudness": sanitize_value(
                    song_info["audio_features"]["loudness"]
                ),

                "tempo": sanitize_value(
                    song_info["audio_features"]["tempo"]
                )

            }

            for song_info in h5_data_list

        ]


        # 批量寫入 AudioFeatures

        session.bulk_insert_mappings(
            AudioFeatures,
            audio_features_mappings
        )



        # =========================
        # 4. 提交資料
        # =========================

        session.commit()


        print(
            f"Successfully inserted {len(h5_data_list)} records."
        )


    except Exception as e:

        # 發生錯誤取消此次操作

        session.rollback()

        print(
            f"Bulk insert error: {e}"
        )

def process_h5_files_in_batches(
    h5_files: list,
    engine,
    batch_size: int = 1000
):

    current_batch_data = []


    for file_path in h5_files:

        try:

            # 開啟 HDF5 檔案
            h5 = hdf5_getters.open_h5_file_read(file_path)


            # 取得歌曲數量
            num_songs = hdf5_getters.get_num_songs(h5)


            # 逐首歌曲處理
            for i in range(num_songs):

                song_info = extract_h5_info(h5, i)

                current_batch_data.append(song_info)


                # 達到批次大小就寫入資料庫
                if len(current_batch_data) >= batch_size:


                    with create_session(engine) as session:

                        insert_song_data_bulk_mappings(
                            session,
                            current_batch_data
                        )


                    # 清空目前批次
                    current_batch_data = []


            # 關閉 H5 檔案
            h5.close()


        except Exception as e:

            print(
                f"Error processing {file_path}: {e}"
            )



    # 處理最後不足 batch_size 的資料

    if current_batch_data:

        with create_session(engine) as session:

            insert_song_data_bulk_mappings(
                session,
                current_batch_data
            )

        current_batch_data = []

if __name__ == "__main__":


    # Million Song Dataset 路徑

    root_dir = "dataset/MillionSongSubset"


    h5_files = glob.glob(
        os.path.join(
            root_dir,
            "**/*.h5"
        ),
        recursive=True
    )


    print(
        f"Found {len(h5_files)} h5 files"
    )


    # PostgreSQL 連線

    engine_url = (
        "postgresql://username:password@localhost:5432/music_database"
    )


    engine = create_engine(
        engine_url,
        echo=True
    )



    # 重建資料表

    print("Dropping existing tables...")

    drop_table(engine)


    print("Creating new tables...")

    create_table(engine)



    print(
        "Starting data processing and insertion..."
    )


    # 開始處理資料

    process_h5_files_in_batches(
        h5_files,
        engine,
        batch_size=1000
    )


    print(
        "Data insertion complete."
    )

