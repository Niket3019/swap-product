from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .services import email
from django.template.loader import render_to_string
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'diy_web_pp/home.html')

def add(request):
    return render(request, 'diy_web_pp/add.html')

@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    return render(request, 'diy_web_pp/cart.html', {'cart_items': cart_items, 'total': total})

def contact(request):
    return render(request, 'diy_web_pp/contact.html')

def design_studio(request):
    return render(request, 'diy_web_pp/design-studio.html')

def login_view(request):
    return render(request, 'diy_web_pp/login.html')

def second_shop(request):
    return render(request, 'diy_web_pp/second_shop.html')

def sell_clothes(request):
    return render(request, 'diy_web_pp/sell-clothes.html')

def shop(request):
    products = Product.objects.all()
    return render(request, 'diy_web_pp/shop.html', {'products': products})

def sproduct(request):
    return render(request, 'diy_web_pp/sproduct.html')

def swap_items(request):
    return render(request, 'diy_web_pp/swap-items.html')

def desing_studio(request):
    return render(request, 'diy_web_pp/desing-studio.html')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

from django.views.decorators.http import require_POST
from django.contrib import messages

@login_required
@require_POST
def update_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart')

@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout_view(request):
    if request.method == 'POST':
        total_amount = request.POST.get('total_amount')
        order = Order.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            card_name=request.POST.get('card_name'),
            card_number=request.POST.get('card_number'),
            expiry_month=request.POST.get('expiry_month'),
            expiry_year=request.POST.get('expiry_year'),
            cvv=request.POST.get('cvv'),
            total_amount=total_amount
        )
        cart_list_obj = CartItem.objects.filter(user=request.user)
        for cart_obj in cart_list_obj:
            OrderItem.objects.create(
                user = cart_obj.user,
                order = order,
                product = cart_obj.product,
                total_amount = float(cart_obj.product.price) * float(cart_obj.quantity)
            )
        CartItem.objects.filter(user=request.user).delete()        
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    padding: 20px;
                    color: #333;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    max-width: 600px;
                    margin: 0 auto;
                }}
                h2 {{
                    color: #4CAF50;
                }}
                .order-details {{
                    margin-top: 20px;
                    border-collapse: collapse;
                    width: 100%;
                }}
                .order-details th, .order-details td {{
                    padding: 10px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                .footer {{
                    margin-top: 30px;
                    font-size: 12px;
                    color: #777;
                }}
                .footer p {{
                    margin: 5px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>✅ Thank you for your order, {request.user.first_name}!</h2>
                <p>Your order has been successfully placed. Here are your order details:</p>

                <table class="order-details">
                    <tr><th>Order ID</th><td>#{order.id}</td></tr>
                    <tr><th>Customer Name</th><td>{request.POST.get('full_name')}</td></tr>
                    <tr><th>Email</th><td>{request.user.email}</td></tr>
                    <tr><th>Shipping Address</th><td>{order.address}</td></tr>
                    <tr><th>Total Amount</th><td>Rs. {order.total_amount}</td></tr>
                </table>

                <p>If you have any questions about your order, feel free to contact us.</p>

                <div class="footer">
                    <p>Best regards, <br>Your Store Team</p>
                    <p>Visit our website: www.yourstore.com</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Subject of the email
        subject = f"🧾 Order Confirmation - #{order.id}"

        # Send email
        email.send_mail_admin(request.user.username, subject, html_message)

        return redirect('order_success', order_id=order.id)
    return render(request, 'diy_web_pp/cart.html')

@login_required
def order_success_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'diy_web_pp/success.html', {'order': order})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Try to authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the homepage or a dashboard after successful login
        else:
            messages.error(request, "Invalid login credentials.")
            return render(request, 'diy_web_pp/login.html')  # Return the same login form with error message

    return render(request, 'diy_web_pp/login.html')  # GET request - render the login form


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

def register_user(request):
    if request.method == 'POST':
        print("===========>run")
        name = request.POST.get('name')
        email_id = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('login')  # Redirect back to the registration page

        # Check if the email already exists
        if User.objects.filter(username=email_id).exists():
            messages.error(request, "Email is already registered.")
            return redirect('login')  # Redirect back to the registration page

        # Create the user
        user = User.objects.create_user(username=email_id, password=password, first_name=name)
        user.save()

        # Send email using your existing send_mail_admin function
        subject = f"Welcome, {name}!"
        message = f"Hello {name},\n\nThank you for registering with us! We're excited to have you on board.\n\nBest regards,\nThe Team"

        # Send the email using your custom function
        email.send_mail_admin(email_id, subject, message)

        messages.success(request, "You have successfully registered! A confirmation email has been sent.")
        return redirect('home')  # Redirect to the home page or another page after registration

    return render(request, 'diy_web_pp/login.html')  # GET request - render the registration page
 
from django.utils.timezone import localtime
from django.db.models import Q

@login_required
def my_orders(request):
    order_items = OrderItem.objects.filter(user=request.user) \
        .select_related('product') \
        .order_by('-created_at')
    orders = []
    for item in order_items:
        orders.append({
            'image_path': item.product.image_path,
            'product_name': item.product.product_name,
            'brand_name': item.product.brand_name,
            'price': item.product.price,
            'rating': item.product.rating,
            'created_at': localtime(item.created_at).strftime('%d %b %Y %H:%M'),
            'total_amount': item.total_amount,
        })
    swap_requests = SwapRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
        is_accepted=True
    ).select_related('from_item', 'to_item').prefetch_related('from_item__images', 'to_item__images')

    for swap in swap_requests:
        # If you are the sender, you get to_item
        if swap.from_user == request.user:
            received_item = swap.to_item
        else:
            # If you are the receiver, you get from_item
            received_item = swap.from_item

        image = received_item.images.first()
        orders.append({
            'image_path': image.image.url if image else '',
            'product_name': received_item.name,
            'brand_name': received_item.condition,
            'price': received_item.price,
            'rating': 'N/A',
            'created_at': localtime(swap.created_at).strftime('%d %b %Y %H:%M'),
            'total_amount': 'Swapped',
            'source': 'swap'
        })

    return render(request, 'diy_web_pp/my_orders.html', {'orders': orders})

@login_required
def swap_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        image_file = request.FILES.get('image')

        item = Item.objects.create(
            user=request.user,
            name=name,
            description=description,
            price=price,
            condition=condition,
            status='available'
        )

        if image_file:
            ItemImage.objects.create(item=item, image=image_file)

        messages.success(request, 'Item swap request saved successfully. You will be notified once a user swaps your product.')
        return redirect('swap-items')

    return render(request, 'diy_web_pp/swap-items.html')

@login_required
def browse_items(request):
    # Exclude current user's items
    items = Item.objects.filter(status='available').exclude(user=request.user)
    user_swap_item = Item.objects.filter(status='available',user=request.user)
    return render(request, 'diy_web_pp/browse_items.html', {'items': items,"user_swap_item":user_swap_item})

def logout_view(request):
    logout(request)
    return redirect('login')  # or any page you want

@login_required
def send_swap_request(request, item_id):
    if request.method == 'POST':
        user_product_id = request.POST.get('userProduct')
        user_product = get_object_or_404(Item, id=user_product_id)
        target_item = get_object_or_404(Item, id=item_id)

        # Prevent duplicate swap requests
        swap, created = SwapRequest.objects.get_or_create(
            from_user=request.user,
            from_item=user_product,
            to_user=target_item.user,
            to_item=target_item
        )

        # Send email to both users involved in the swap
        subject = f"🔄 New Swap Request for Your Item - #{swap.id}"
        message = f"Hello, you have a new swap request. Your item '{user_product.name}' is requested to be swapped for '{target_item.name}'."

        # Send email to the user who is offering the swap (the target user)
        email.send_mail_admin(target_item.user.username, subject, message)

        # Optionally, send a confirmation email to the user who initiated the swap (if needed)
        confirmation_message = f"Your swap request has been sent successfully. You are offering '{user_product.name}' in exchange for '{target_item.name}'."
        print(confirmation_message)
        email.send_mail_admin(request.user.username, subject, confirmation_message)
        return redirect('chat_view', swap_id=swap.id)
    
@login_required
def chat_view(request, swap_id):
    swap = get_object_or_404(SwapRequest, id=swap_id)
    print("=======>to_user",swap.to_user.username)
    print("current_user",request.user.username)
    # Ensure user is involved
    if request.user not in [swap.from_user, swap.to_user]:
        return redirect('home')

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            ChatMessage.objects.create(
                swap=swap,
                sender=request.user,
                message=message_text
            )

    messages = swap.messages.order_by('timestamp')
    return render(request, 'diy_web_pp/chat_view.html', {
        'swap': swap,
        'messages': messages,
        'user': request.user,
    })
from django.http import JsonResponse

def swap_notification(request):
    # Get the user_id from the request query parameters
    user_id = request.GET.get('user_id')
    
    if user_id:
        swap_notifications = SwapRequest.objects.filter(to_user__id=user_id)

        # Prepare data to send to the frontend
        data = [
            {
                'swap_id': notification.id,
                'user_id': notification.from_user.id,
                'username': notification.from_user.username,
                'product_name': notification.from_item.name,
                'product_condition': notification.from_item.condition,
                'is_accepted': notification.is_accepted,
            }
            for notification in swap_notifications
        ]
        
        return JsonResponse(data, safe=False)
    
    return JsonResponse({'error': 'User ID not provided'}, status=400) 

@csrf_exempt
def accept_swap(request):
    if request.method == 'POST':
        swap_id = request.POST.get('swap_id')
        try:
            swap = SwapRequest.objects.get(id=swap_id)
            swap.is_accepted = True
            swap.save()
            Item.objects.filter(id__in=[swap.from_item.id, swap.to_item.id]).update(status='sold')
            subject = f"🧾 Order Confirmation - Swap Accepted for #{swap_id}"
            message = f"Hello, your swap request #{swap_id} has been accepted! Both items are now marked as sold."
            email.send_mail_admin(swap.from_item.user.username, subject, message)
            email.send_mail_admin(swap.to_item.user.username, subject, message)
            print("accespted")
        except SwapRequest.DoesNotExist:
            pass
        return redirect('swap-items')  # Or wherever you want to go
    
@login_required
def swap_requests_view(request):
    user = request.user

    sent_requests = SwapRequest.objects.filter(from_user=user) \
        .select_related('from_item') \
        .prefetch_related(
            'from_item__images'  # Prefetch images for from_item
        )

    received_requests = SwapRequest.objects.filter(to_user=user) \
        .select_related( 'to_item') \
        .prefetch_related(
            'to_item__images'  # Prefetch images for from_item
        )

    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }

    return render(request, 'diy_web_pp/swap_chat.html', context)