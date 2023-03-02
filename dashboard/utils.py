from tiffine_site.models import Cart
from order.models import OrderModel
from django.utils import timezone
from django.db.models import QuerySet
import datetime

def get_qs_timeslot(query:QuerySet) -> QuerySet:
    """Current day delivery items"""
    timeslot = query.get('type', day_part_filter())
    
    if query.get('filter'):
        return OrderModel.objects.filter(
            cart__is_complete = True,
            order_status='PENDING',
            time_slot__icontains=timeslot,
            address__city=query.get('filter'))
    
    # return OrderModel.objects.filter(cart__is_complete = True, created_at__date=datetime.date.today(), created_at__time=current_time, order_status='PENDING', time_slot=timeslot)
    return OrderModel.objects.filter(
        cart__is_complete = True, 
        order_status='PENDING', 
        time_slot__icontains=timeslot)

def day_part_filter():
    """return day park filter"""
    current_time = timezone.now().time()
    beakfast = datetime.time(12,45,00)
    lunch = datetime.time(14,45,00)
    dinner = datetime.time(21,45,00)

    if current_time < beakfast:
        return 'BREAKFAST'
    elif current_time < lunch:
        return 'LUNCH'
    elif current_time < dinner:
        return 'DINNER'
    else:
        return 'BREAKFAST'