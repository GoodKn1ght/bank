from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import User, Person, Extract
from datetime import datetime
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializer import UserSerializer


def userreg(request):
    return render(request, 'myapp/userreg.html', {})

def insertuser(request):
    vuid = request.POST['tuid']
    vuname = request.POST['tuname']
    vuemail = request.POST['tuemail']
    vucontact = request.POST['tucontact']
    vudoc = request.POST['tudoc']
    vupass = request.POST['tupass']
    vums = request.POST['tums']
    terms = '1'
    per = Person(ID=vuid, Phone_Number=vucontact, Documents=vudoc, Email=vuemail)
    per.save()
    us = User(
        ID=vuid,
        Terms_Of_Use=terms,
        Hashed_Password=vupass,
        Mother_Surname=vums,
        Money_Left=1000.0,
        User_Created=datetime.now()
    )
    us.save()
    request.session['user_id'] = us.ID  # Зберегти ID у сесії
    request.session['balance'] = float(us.Money_Left)
    return redirect('user_profile')  # виконує перенаправлення на user_profile

def user_profile(request):
    us = request.user  # Отримання поточного користувача
    return render(request, 'myapp/user_profile.html', {'us': us})




def userextract(request):
    user_id = request.session.get('user_id')  # Отримуємо ID користувача з сесії
    if not user_id:
        return redirect('userlog')  # Якщо ID не знайдено, перенаправляємо на сторінку входу

    with connection.cursor() as cursor:
        cursor.callproc('TakeExtract', [user_id])

        total_summary = cursor.fetchall()

        cursor.nextset()
        columns = [col[0] for col in cursor.description]
        operation_details = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return render(request, "myapp/user_extract.html", {
        'total_summary': total_summary,
        'operation_details': operation_details
    })



def transfer_funds(request, sender_id):
    if request.method == 'POST':
        receiver_id = int(request.POST['receiver_id'])
        transfer_amount = float(request.POST['transfer_amount'])
        choice = bool(int(request.POST['choice']))  # 1 or 0 for True/False

        try:
            with connection.cursor() as cursor:
                cursor.callproc('transfer_funds', [sender_id, receiver_id, transfer_amount, choice])
            with connection.cursor() as cursor:
                cursor.execute("SELECT Money_Left FROM user WHERE ID = %s", [sender_id])
                balance = cursor.fetchone()
                if balance:
                    request.session['balance'] = float(balance[0])  # Convert to float before saving

            messages.success(request, 'Transfer completed successfully!')
            return redirect('user_profile')
        except Exception as e:
            messages.error(request, f'Error during transfer: {str(e)}')
            return redirect('user_profile')

    return render(request, 'myapp/transfer_funds.html')


def userlog(request):
    return render(request, 'myapp/userlog.html')


def loginuser(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        try:
            user = User.objects.get(ID=user_id)
            if user.Hashed_Password == password:
                request.session['user_id'] = user.ID
                request.session['balance'] = float(user.Money_Left)
                return redirect('user_profile')
            else:
                messages.error(request, 'Неправильний ID або пароль')
        except User.DoesNotExist:
            messages.error(request, 'Користувача з таким ID не існує')

    return redirect('userlog')

def delete_current_user(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:

            user = User.objects.get(ID=user_id)
            user.delete()
            messages.success(request, 'Ваш акаунт успішно видалено.')

            del request.session['user_id']
        except User.DoesNotExist:
            messages.error(request, 'Користувача з таким ID не існує.')
    else:
        messages.error(request, 'Ви не увійшли в систему.')

    return redirect('userreg')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(ID__range=(1, 100))
    serializer_class = UserSerializer


def user_create(request):
    if request.method == 'POST':
        # Отримуємо дані з форми або POST запиту
        vuid = request.data.get('tuid')
        vuname = request.data.get('tuname')
        vuemail = request.data.get('tuemail')
        vucontact = request.data.get('tucontact')
        vudoc = request.data.get('tudoc')
        vupass = request.data.get('tupass')
        vums = request.data.get('tums')
        terms = '1'

        # Спочатку створюємо запис у таблиці person_info
        try:
            # Перевіряємо чи вже існує такий ID для Person
            if not Person.objects.filter(ID=vuid).exists():
                per = Person(ID=vuid, Phone_Number=vucontact, Documents=vudoc, Email=vuemail)
                per.save()  # Зберігаємо персону в базі даних

                # Після того, як персону збережено, створюємо запис у таблиці user
                us = User(
                    ID=vuid,
                    Terms_Of_Use=terms,
                    Hashed_Password=vupass,
                    Mother_Surname=vums,
                    Money_Left=1000.0,  # Початковий баланс
                    User_Created=datetime.now(),
                    Person=per  # Вказуємо зв'язок через зовнішній ключ
                )
                us.save()  # Зберігаємо користувача

                return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

            else:
                return Response({'error': 'Person with this ID already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def user_list(request):
    view = UserViewSet.as_view({'get': 'list'})
    return view(request)

def user_retrieve(request, pk):
    view = UserViewSet.as_view({'get': 'retrieve'})
    return view(request, pk=pk)

def user_update(request, pk):
    view = UserViewSet.as_view({'put': 'update', 'patch': 'partial_update'})
    return view(request, pk=pk)

def user_delete(request, pk):
    view = UserViewSet.as_view({'delete': 'destroy'})
    return view(request, pk=pk)