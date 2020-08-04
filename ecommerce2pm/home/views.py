from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View, DetailView

from home.models import Item, Ad, Brand, Slider, OrderItem, Order

from .models import OrderItem


class BaseView(View):
    views = {

    }

class HomeView(BaseView):
    def get(self, request):
        self.views['items'] = Item.objects.all()
        self.views['new'] = Item.objects.filter(labels='new')
        self.views['hot'] = Item.objects.filter(labels='hot')
        self.views['sale'] = Item.objects.filter(labels='sale')
        self.views['ads'] = Ad.objects.all()
        self.views['brands'] = Brand.objects.all()
        self.views['slider'] = Slider.objects.all()
        return render(self.request, 'shop-index.html', self.views)

class ItemDetailVIew(DetailView):
    model = Item
    template_name = 'shop-item.html'

class SearchView(BaseView):
    def get(self, request):
        search = request.GET.get('query', None)
        if not search:
            return redirect ('/')

        self.views['search_result'] = Item.objects.filter(
            title__icontains = search
        )
        self.views['search'] = search
        return render(self.request, 'shop-search-result.html', self.views)

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'This is username is already exists.')
                return redirect("home:signup")

            elif User.objects.filter(email = email).exists():
                messages.error(request, 'This is email is already exists.')
                return redirect("home:signup")

            else:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password,
                    first_name = first_name,
                    last_name = last_name

                )
                user.save()
                return redirect("/accounts/login")

        else:
            messages.error(request, 'Passwords do not match')
            return redirect("home:signup")




    return render(request, 'signup.html')

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )[0]
    orders = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if orders.exists():
        order = orders[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request,"The quantity is updated")
            return redirect('home:order')
        else:
            order.items.add()
            messages.success(request, "The product is added")
            return redirect('home:order')

    else:
        order = Order.objects.create(
            user = request.user,
        )
        order.items.add(order_item)
        messages.success(request, "Success!!! Product is added")
        return redirect('home:order')


class OrderSummaryView(BaseView):
    def get(self,*arg, **kwargs):
        try:
            order = Order.objects.get(
                user = self.request.user,
                ordered = False
            )
            self.views['object'] = order

        except:
            messages.error(self.request,"Some error occured")
            return redirect('/')

        return render(self.request, 'shop-shopping-cart.html',self.views)


#db browser for SQLite