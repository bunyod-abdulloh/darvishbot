from utils.db_api.create_db_tables import Database


class AdditionalDB:
    def __init__(self, db: Database):
        self.db = db

    async def get_doctors(self):
        sql = """ SELECT name FROM clinic_doctor """
        return await self.db.execute(sql, fetchrow=True)

    async def get_patient(self, telegram_id):
        sql = """SELECT * FROM clinic_patient WHERE tg_id = $1"""
        return await self.db.execute(sql, telegram_id, fetchrow=True)

    async def add_patient(self, telegram_id, name, phone, marital_status, absence_children, work, result_eeg):
        sql = """
            INSERT INTO clinic_patient (
                tg_id, name, phone, gender, age, marital_status, absence_children, work, result_eeg
            )
            SELECT 
                $1::VARCHAR, $2::VARCHAR, $3::VARCHAR, gender, age,
                $4::VARCHAR, $5::VARCHAR, $6::VARCHAR, $7::VARCHAR
            FROM bot_users
            WHERE telegram_id = $1::VARCHAR
            RETURNING id
        """
        patient_id = await self.db.execute(
            sql,
            str(telegram_id), name, phone,
            marital_status, absence_children, work, result_eeg,
            fetchval=True
        )

        if patient_id is None:
            print("❌ INSERT bajarilmadi, chunki bot_users da bu telegram_id yo‘q:", telegram_id)

        return patient_id

    async def add_to_tt_eysenc(self, patient_id, temperament, extraversion, neuroticism):
        sql = """INSERT INTO clinic_tt_eysenc (patient_id, temperament, extraversion, neuroticism, create_date) VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP)"""
        return await self.db.execute(sql, patient_id, temperament, extraversion, neuroticism, execute=True)

    async def add_to_tt_yakhin(self, patient_id, neurotic_detected, anxiety, depression, asthenia, hysteroid_response,
                               obsessive_phobic, vegetative):
        sql = """INSERT INTO clinic_tt_yakhin (patient_id, neurotic_detected, anxiety, depression, asthenia, 
                hysteroid_response, obsessive_phobic, vegetative, create_date) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, CURRENT_TIMESTAMP)"""
        return await self.db.execute(sql, patient_id, neurotic_detected, anxiety, depression, asthenia,
                                     hysteroid_response, obsessive_phobic, vegetative, execute=True)

    async def add_tt_leonhard(self, patient_id, hysteroid, pedantic, rigid, epileptoid, hyperthymic, dysthymic, anxious,
                              cyclothymic, affective, emotive):
        sql = """INSERT INTO clinic_tt_leonhard (patient_id, hysteroid, pedantic, rigid, epileptoid, hyperthymic, 
                dysthymic, anxious, cyclothymic, affective, emotive, create_date) 
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, CURRENT_TIMESTAMP)"""
        return await self.db.execute(sql, patient_id, hysteroid, pedantic, rigid, epileptoid, hyperthymic, dysthymic,
                                     anxious, cyclothymic, affective, emotive, execute=True)
