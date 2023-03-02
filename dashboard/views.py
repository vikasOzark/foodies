from django.shortcuts import render, redirect
from django.views import generic
from order.models import OrderModel
from .utils import get_qs_timeslot, day_part_filter
from django.utils import timezone
from django.db.models import Sum, Count, QuerySet
from tiffine_site.models import Items, MainDishModel


class DashbordViews(generic.list.ListView):
    template_name =  'superadmin.html'
    page_kwarg = 'id'
    context_object_name = 'orders'
    
    def get_queryset(self, *args, **kwargs):
        query = self.request.GET
        if query.get('type') == 'complete':
            return OrderModel.delivered.all()
        return get_qs_timeslot(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET
        timeslot = query.get('type', day_part_filter()).lower()

        location = OrderModel.objects.filter(
                order_status='PENDING', 
                time_slot__icontains=timeslot
            ).values('address__city').annotate(total=Count('address__city'))

        context['type'] = timeslot
        context['location'] = location
        return context
        
    
class OrderDetail(generic.DetailView):
    model = OrderModel
    template_name='order_detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'order'
    

class KitchenView(generic.View):
    def get(self, *args, **kwargs):
        template_name='kitchen.html'
        context ={}
        context['items'] = self.get_queryset(*args, **kwargs)
        return render(self.request, template_name, context)
    
    def get_queryset(self, *args, **kwargs):
        # TODO need to add filter option
        food_ids = []
        print(day_part_filter())
        order_object = OrderModel.objects.filter(time_slot=day_part_filter())
        for obj in order_object:
            item_ids = obj.cart.get_cart_items().values_list('food__id', flat=True)
            for i in item_ids:
                food_ids.append(i)
        return Items.objects.filter(food__id__in=food_ids).values('food__name').annotate(total=Count('food__name'))

class LocationOrder(generic.View):
    def get(self, *args, **kwargs):
        location = kwargs.get('location')
        timeslot = self.request.GET.get('timeslot')
        
        template_name = 'location_order.html'
        context = {}
        context['items'] = self.get_queryset(location, timeslot)
        context['location'] = location
        return render(self.request, template_name, context)
    

    def get_queryset(self, location:str, timeslot:str) -> QuerySet:
        # TODO need to add filter option for time slot
        food_ids = []
        order_object = OrderModel.objects.filter(address__city=location, time_slot__icontains=timeslot)
        for obj in order_object:
            item_ids = obj.cart.get_cart_items().values_list('food__id', flat=True)
            for i in item_ids:
                food_ids.append(i)
        return Items.objects.filter(food__id__in=food_ids).values('food__name').annotate(total=Count('food__name'))
    

def mark_complete(request, pk):
    obj = OrderModel.objects.get(pk=pk)
    obj['order_status'] = 'DELIVERD'
    obj.save()
    return redirect('dashboard')

def mark_complete(request, pk):
    obj = OrderModel.objects.get(pk=pk)
    print(obj)
    obj.order_status = 'DELIVERD'
    obj.save()
    return redirect('dashboard')

def mark_cancel(request, pk):
    obj = OrderModel.objects.get(pk=pk)
    obj['order_status'] = 'CANCEL'
    obj.save()
    return redirect('dashboard')