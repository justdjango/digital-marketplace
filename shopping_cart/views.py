from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from books.models import Book
from .models import Order, OrderItem, Payment
import stripe
import string
import random

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))


@login_required
def add_to_cart(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item, created = OrderItem.objects.get_or_create(book=book)
    order, created = Order.objects.get_or_create(user=request.user)
    order.items.add(order_item)
    order.save()
    messages.info(request, "Item successfully added to your cart.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def remove_from_cart(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item = get_object_or_404(OrderItem, book=book)
    order = get_object_or_404(Order, user=request.user)
    order.items.remove(order_item)
    order.save()
    messages.info(request, "Item successfully removed from your cart.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def order_view(request):
    order = get_object_or_404(Order, user=request.user)
    context = {
        'order': order
    }
    return render(request, "order_summary.html", context)


@login_required
def checkout(request):
    order = get_object_or_404(Order, user=request.user)
    if request.method == "POST":

        try:
            # complete the order (ref code and set ordered to true)
            order.ref_code = create_ref_code()

            # create a stripe charge
            token = request.POST.get('stripeToken')
            charge = stripe.Charge.create(
                amount=int(order.get_total() * 100),  # cents
                currency="usd",
                source=token,  # obtained with Stripe.js
                description=f"Charge for {request.user.username}"
            )

            # create our payment object and link to the order
            payment = Payment()
            payment.order = order
            payment.stipe_charge_id = charge.id
            payment.total_amount = order.get_total()
            payment.save()

            # add the book to the users book list
            books = [item.book for item in order.items.all()]
            for book in books:
                request.user.userlibrary.books.add(book)

            order.is_ordered = True
            order.save()

            # redirect to the users profile
            return redirect("/account/profile/")

        # send email to yourself

        except stripe.error.CardError as e:
            messages.error(request, "There was a card error.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.RateLimitError as e:
            messages.error(request, "There was a rate limit error on Stripe.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.InvalidRequestError as e:
            messages.error(request, "Invalid parameters for Stripe request.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.AuthenticationError as e:
            messages.error(request, "Invalid Stripe API keys.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.APIConnectionError as e:
            messages.error(
                request, "There was a network error. Please try again.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.StripeError as e:
            messages.error(request, "There was an error. Please try again.")
            return redirect(reverse("cart:checkout"))
        except Exception as e:
            messages.error(
                request, "There was a serious error. We are working to resolve the issue.")
            return redirect(reverse("cart:checkout"))

    context = {
        'order': order
    }

    return render(request, "checkout.html", context)
