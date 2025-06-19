from app.services.reservation.ReservationService import ReservationServiceImpl
from app.services.reservation.TableService import TableServiceImpl

def try_make_reservation(db_session, user_context, reservation_data):
    """
    Verilen bilgilere göre uygun masa aranır, varsa rezervasyon yapılır.
    Masa tercihi (örn. Window) varsa dikkate alınır.
    """

    # 1. Zorunlu alanları kontrol et
    required_fields = ["date", "time", "guest_count"]
    missing_fields = [field for field in required_fields if not reservation_data.get(field)]

    if missing_fields:
        return None, f"⚠️ Rezervasyon işlemi için eksik bilgiler var: {', '.join(missing_fields)}"

    # 2. Servisleri başlat
    restaurant_id = user_context.get("restaurant_id", 1)
    preferred_location = reservation_data.get("preferred_location")

    table_service = TableServiceImpl(db_session)
    reservation_service = ReservationServiceImpl(db_session)

    # 3. Uygun masa ara
    available_tables = table_service.get_available_tables(
        restaurant_id=restaurant_id,
        res_date=reservation_data["date"],
        res_time=reservation_data["time"],
        guest_count=reservation_data["guest_count"],
        preferred_location=preferred_location
    )

    if not available_tables:
        return None, "⚠️ Maalesef bu tarih ve saatte uygun masa bulunamadı."

    selected_table = available_tables[0]

    # 4. Rezervasyonu oluştur
    reservation = reservation_service.create_reservation(
        user_name=user_context.get("name", "Guest"),
        phone=user_context.get("phone", ""),
        email=user_context.get("email", ""),
        date=reservation_data["date"],
        time=reservation_data["time"],
        guest_count=reservation_data["guest_count"],
        table_id=selected_table.id,
        source="chat"
    )

    message = f"✅ Rezervasyon oluşturuldu: {selected_table.capacity} kişilik masa ({selected_table.table_code})."
    return reservation, message

