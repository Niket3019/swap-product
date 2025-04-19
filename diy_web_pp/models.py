from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    brand_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_path = models.CharField(max_length=255)  # path relative to static/
    created_at = models.DateTimeField(auto_now_add=True,null=True)  # 👈 this adds the timestamp only once when created

    def __str__(self):
        return f"{self.brand_name} - {self.product_name}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevents duplicate product entries for the same user

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    card_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20)
    expiry_month = models.CharField(max_length=20)
    expiry_year = models.IntegerField()
    cvv = models.CharField(max_length=10)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.full_name}"
    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_item')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OrderItem #{self.id} by {self.user.email}"
    
class Item(models.Model):
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Like New', 'Like New'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Used', 'Used'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=20, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Item #{self.user.first_name} by {self.user.email}"
class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_images/')
    def __str__(self):
        return f"ItemImage #{self.item.user.first_name} by {self.item.user.email}"

class SwapRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="swap_sent", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="swap_received", on_delete=models.CASCADE)
    from_item = models.ForeignKey(Item, related_name="swap_from", on_delete=models.CASCADE)
    to_item = models.ForeignKey(Item, related_name="swap_to", on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SwapRequest # {self.from_user} ↔ {self.to_user} | {self.from_item.name} ⇄ {self.to_item.name}"
    
class ChatMessage(models.Model):
    swap = models.ForeignKey(SwapRequest, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatMessage # {self.sender.username}: {self.message[:30]}"

