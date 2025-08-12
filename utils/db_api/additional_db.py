from utils.db_api.create_db_tables import Database


class AdditionalDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== PATIENT DATAS ===========================
    async def get_patient(self, telegram_id):
        sql = """SELECT * FROM clinic_patient WHERE tg_id = $1"""
        return await self.db.execute(sql, telegram_id, fetchrow=True)

    async def get_patient_by_id(self, patient_id):
        sql = """SELECT tg_id, name FROM clinic_patient WHERE id = $1"""
        return await self.db.execute(sql, patient_id, fetchrow=True)

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

    async def delete_patient_datas(self, patient_telegram):
        await self.db.execute("""DELETE FROM clinic_patient WHERE tg_id = $1""", patient_telegram, execute=True)

    async def set_fullname(self, fullname, telegram_id):
        sql = """UPDATE clinic_patient SET name = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, fullname, telegram_id, execute=True)

    async def set_gender(self, gender, telegram_id):
        sql = """UPDATE clinic_patient SET gender = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, gender, telegram_id, execute=True)

    async def set_age(self, age, telegram_id):
        sql = """UPDATE clinic_patient SET age = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, age, telegram_id, execute=True)

    async def set_phone(self, phone, telegram_id):
        sql = """UPDATE clinic_patient SET phone = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, phone, telegram_id, execute=True)

    async def set_marital_status(self, marital_status, telegram_id):
        sql = """UPDATE clinic_patient SET marital_status = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, marital_status, telegram_id, execute=True)

    async def set_absence_children(self, absence_children, telegram_id):
        sql = """UPDATE clinic_patient SET absence_children = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, absence_children, telegram_id, execute=True)

    async def set_work(self, work, telegram_id):
        sql = """UPDATE clinic_patient SET work = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, work, telegram_id, execute=True)

    async def set_result_eeg(self, result_eeg, telegram_id):
        sql = """UPDATE clinic_patient SET result_eeg = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, result_eeg, telegram_id, execute=True)

    # =========================== DOCTOR DATAS ===========================
    async def get_doctor_id(self):
        sql = """ SELECT id FROM clinic_doctor WHERE name = 'Gavhar Darvish' """
        return await self.db.execute(sql, fetchval=True)

    async def get_doctor_work_days(self):
        sql = """SELECT wd.id, wd.code, wd.name, wd.start_hour, wd.end_hour FROM clinic_workday wd 
            JOIN clinic_doctor d ON wd.doctor_id = d.id WHERE d.name = 'Gavhar Darvish' ORDER BY wd.start_hour"""
        return await self.db.execute(sql, fetch=True)

    async def get_doctor_time(self, formatted_date: str):
        sql = """
            SELECT
                TO_CHAR(a.appointment_date, 'HH24:MI') AS appointment_time                    
            FROM clinic_appointment a
            JOIN clinic_doctor d ON a.doctor_id = d.id
            WHERE a.appointment_date::date = $1
              AND d.name = 'Gavhar Darvish'
            ORDER BY a.appointment_date
        """
        return await self.db.execute(sql, formatted_date, fetch=True)

    # =========================== TESTS ===========================
    async def add_to_tt_eysenc(self, patient_id, temperament, extraversion, neuroticism, current_date):

        check_sql = """
        SELECT id FROM clinic_tt_eysenc WHERE patient_id = $1 AND DATE(create_date) = $2
        """
        existing = await self.db.execute(check_sql, patient_id, current_date, fetchval=True)

        if existing:
            update_sql = """
            UPDATE clinic_tt_eysenc SET 
                temperament = $2,
                extraversion = $3,
                neuroticism = $4
            WHERE patient_id = $1
            """
            return await self.db.execute(update_sql, patient_id, temperament, extraversion, neuroticism, execute=True)
        else:
            insert_sql = """
            INSERT INTO clinic_tt_eysenc (
                patient_id, temperament, extraversion, neuroticism, create_date
                )
            VALUES (
                $1, $2, $3, $4, CURRENT_TIMESTAMP
                )
            """
            return await self.db.execute(insert_sql, patient_id, temperament, extraversion, neuroticism, execute=True)


    async def add_to_tt_yakhin(self, patient_id, neurotic_detected, anxiety, depression, asthenia, hysteroid_response,
                               obsessive_phobic, vegetative, current_date):
        check_sql = """
                SELECT id FROM clinic_tt_yakhin WHERE patient_id = $1 AND DATE(create_date) = $2
                """
        existing = await self.db.execute(check_sql, patient_id, current_date, fetchval=True)

        if existing:
            update_sql = """
                    UPDATE clinic_tt_yakhin SET 
                        neurotic_detected = $2,
                        anxiety = $3,
                        depression = $4,
                        asthenia = $5, 
                        hysteroid_response = $6, 
                        obsessive_phobic = $7,
                        vegetative = $8
                    WHERE patient_id = $1
                    """
            return await self.db.execute(update_sql, patient_id, neurotic_detected, anxiety, depression, asthenia,
                                         hysteroid_response, obsessive_phobic, vegetative, execute=True)
        else:
            insert_sql = """
                    INSERT INTO clinic_tt_yakhin (
                        patient_id, neurotic_detected, anxiety, depression, asthenia, hysteroid_response, 
                        obsessive_phobic, vegetative, create_date
                        )
                    VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, CURRENT_TIMESTAMP
                        )
                    """
            return await self.db.execute(insert_sql, patient_id, neurotic_detected, anxiety, depression, asthenia,
                                         hysteroid_response, obsessive_phobic, vegetative, execute=True)


    async def add_tt_leonhard(self, patient_id, hysteroid, pedantic, rigid, epileptoid, hyperthymic, dysthymic, anxious,
                              cyclothymic, affective, emotive, current_date):
        check_sql = """
                    SELECT id FROM clinic_tt_leonhard WHERE patient_id = $1 AND DATE(create_date) = $2
                    """
        existing = await self.db.execute(check_sql, patient_id, current_date, fetchval=True)

        if existing:
            update_sql = """
                        UPDATE clinic_tt_leonhard SET 
                            hysteroid = $2,          
                            pedantic = $3,
                            rigid = $4,
                            epileptoid = $5, 
                            hyperthymic = $6, 
                            dysthymic = $7,
                            anxious = $8,
                            cyclothymic = $9,
                            affective = $10,
                            emotive = $11
                        WHERE patient_id = $1
                        """
            return await self.db.execute(update_sql, patient_id, hysteroid, pedantic, rigid, epileptoid, hyperthymic,
                                         dysthymic, anxious, cyclothymic, affective, emotive, execute=True)
        else:
            insert_sql = """
                        INSERT INTO clinic_tt_leonhard (
                            patient_id, hysteroid, pedantic, rigid, epileptoid, hyperthymic, dysthymic, anxious,
                            cyclothymic, affective, emotive, create_date
                            )
                        VALUES (
                            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, CURRENT_TIMESTAMP
                            )
                        """
            return await self.db.execute(insert_sql, patient_id, hysteroid, pedantic, rigid, epileptoid, hyperthymic,
                                         dysthymic, anxious, cyclothymic, affective, emotive, execute=True)

    async def add_or_update_questionnaire(self, patient_id, headache, dizziness, nausea, abdominal_pain,
                                          feeling_choking, heart_palpitations, sleep_disturbance, low_mood, crying,
                                          indifference, current_date):

        # 1. Avval SELECT qilib tekshirish
        check_sql = """
        SELECT id FROM clinic_tt_questionnaire 
        WHERE patient_id = $1 AND DATE(create_date) = $2
        """
        existing = await self.db.execute(check_sql, patient_id, current_date, fetchval=True)

        if existing:
            # 2. UPDATE qiling
            update_sql = """
            UPDATE clinic_tt_questionnaire SET
                headache = $2,
                dizziness = $3,
                nausea = $4,
                abdominal_pain = $5,
                feeling_choking = $6,
                heart_palpitations = $7,
                sleep_disturbance = $8,
                low_mood = $9,
                crying = $10,
                indifference = $11                
            WHERE patient_id = $1
            """
            return await self.db.execute(update_sql, patient_id, headache, dizziness, nausea, abdominal_pain,
                                         feeling_choking, heart_palpitations, sleep_disturbance, low_mood, crying,
                                         indifference, execute=True)
        else:
            # 3. Yo'q bo'lsa INSERT qiling
            insert_sql = """
            INSERT INTO clinic_tt_questionnaire (
                patient_id, headache, dizziness, nausea, abdominal_pain, feeling_choking, heart_palpitations,
                sleep_disturbance, low_mood, crying, indifference, create_date
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11,CURRENT_TIMESTAMP
            )
            """
            return await self.db.execute(insert_sql, patient_id, headache, dizziness, nausea, abdominal_pain,
                                         feeling_choking, heart_palpitations, sleep_disturbance, low_mood, crying,
                                         indifference, execute=True)

    # =========================== APPOINTMENTS ===========================
    async def add_to_appointments(self, patient_id, doctor_id, company_id, consultation_duration, age_group,
                                  appointment_date):
        sql = """INSERT INTO clinic_appointment (patient_id, doctor_id, company_id, service_type_id, consultation_duration, age_group, appointment_date) 
                VALUES ($1, $2, $3, 1, $4, $5, $6)"""
        return await self.db.execute(sql, patient_id, doctor_id, company_id, consultation_duration, age_group,
                                     appointment_date, execute=True)

    async def get_patient_appointment_date(self, telegram_id):
        sql = """
                SELECT a.appointment_date, a.consultation_duration, p.name FROM clinic_appointment a 
                JOIN clinic_patient p ON a.patient_id = p.id WHERE p.tg_id = $1
                """
        return await self.db.execute(sql, telegram_id, fetchrow=True)

    async def get_appointment_datas(self):
        sql = """
                SELECT patient_id, consultation_duration, appointment_date
                    FROM clinic_appointment
                    WHERE appointment_date::date = CURRENT_DATE + INTERVAL '1 day'
                    ORDER BY appointment_date;
                """
        return await self.db.execute(sql, fetch=True)
