from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .models import User, Person, Extract
from datetime import datetime
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

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


from django.shortcuts import render, redirect
from django.db import connection

def loginuser(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        # Верифікація користувача (залежить від вашої логіки)
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID, Money_Left FROM user WHERE ID = %s AND password = %s", [user_id, password])
            user = cursor.fetchone()

        if user:
            # Збереження даних користувача в сесію
            request.session['user_id'] = user[0]
            request.session['balance'] = float(user[1])  # Баланс
            messages.success(request, 'Ви успішно увійшли!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Неправильний ID або пароль!')

    return render(request, 'myapp/login.html')

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

# yourapp/views.py

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


from django.shortcuts import redirect
from django.contrib import messages
from django.db import connection

from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import connection


def transfer_funds(request, sender_id):
    if request.method == 'POST':
        receiver_id = int(request.POST['receiver_id'])
        transfer_amount = float(request.POST['transfer_amount'])
        choice = bool(int(request.POST['choice']))  # 1 або 0 для True/False

        try:
            # Виконання процедури транзакції
            with connection.cursor() as cursor:
                cursor.callproc('transfer_funds', [sender_id, receiver_id, transfer_amount, choice])

            # Оновлення балансу в сесії
            with connection.cursor() as cursor:
                cursor.execute("SELECT Money_Left FROM users_user WHERE ID = %s", [sender_id])
                balance = cursor.fetchone()
                if balance:
                    request.session['balance'] = float(balance[0])  # Зберігаємо актуальний баланс у сесії

            # Повідомлення про успіх
            messages.success(request, 'Транзакція успішно виконана!')
            return redirect('user_profile')  # Повертаємо користувача до його профілю
        except Exception as e:
            # Повідомлення про помилку
            messages.error(request, f'Помилка під час транзакції: {str(e)}')
            return redirect('user_profile')

    return render(request, 'myapp/transfer_funds.html')


from django.http import JsonResponse
from django.db import connection

def get_balance(request):
    user_id = request.session.get('user_id')
    if user_id:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Money_Left FROM user WHERE ID = %s", [user_id])
            balance = cursor.fetchone()
        if balance:
            return JsonResponse({'balance': float(balance[0])})
    return JsonResponse({'balance': 0})

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

from django.shortcuts import render
from django.db import connection
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource

def fetch_data_office_summary():
    query = """
        SELECT e.Office, COUNT(*) AS Employee_Count
        FROM employee e
        JOIN person_info p ON e.ID = p.ID
        GROUP BY e.Office
        HAVING Employee_Count > 0;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    columns = ['Office', 'Employee_Count']
    return pd.DataFrame(rows, columns=columns)


def bokeh_office_summary(request):
    # Fetch data
    df = fetch_data_office_summary()

    # Create Bokeh plot
    source = ColumnDataSource(df)

    plot_width = max(800, len(df['Office']) * 100)
    p = figure(x_range=df['Office'], title="Employee Count per Office",
               x_axis_label="Office", y_axis_label="Employee Count",
               height=500, width=plot_width)

    p.vbar(x='Office', top='Employee_Count', width=0.5, source=source, color="blue", alpha=0.7)
    p.xaxis.major_label_orientation = 1.2  # Rotate X-axis labels
    p.xgrid.grid_line_color = None         # Remove vertical grid lines

    # Embed the plot in the template
    plot_html = file_html(p, CDN, "Office Summary")
    return render(request, 'myapp/bokeh_office_summary.html', {'bokeh_plot': plot_html})


from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN
import plotly.express as px


# Fetch data for maximum used balance
def fetch_data_max_balance():
    query = """
        SELECT u.ID, MAX(o.Money_Used) as Max_Amount 
        FROM operation o
        JOIN user u ON u.ID = o.User_ID
        GROUP BY u.ID
        ORDER BY Max_Amount DESC
        LIMIT 100;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    df['Max_Amount'] = df['Max_Amount'].astype(float)  # Ensure numeric type for plotting
    return df


# Bokeh plot for max balance
def bokeh_max_balance(request):
    df = fetch_data_max_balance()
    df['ID'] = df['ID'].astype(str)  # Ensure string type for x-axis labels

    source = ColumnDataSource(df)

    p = figure(title="Max Money Used by Each User",
               x_axis_label="User ID", y_axis_label="Max Money Used",
               height=500, width=1500, x_range=df['ID'].tolist())

    p.line(x='ID', y='Max_Amount', source=source, line_width=2, color="orange", legend_label="Max Amount")
    p.xaxis.major_label_orientation = "vertical"
    p.legend.location = "top_left"
    p.legend.background_fill_color = "white"

    # Embed the plot in HTML template
    plot_html = file_html(p, CDN, "Max Balance")
    return HttpResponse(plot_html)


# Plotly plot for max balance
def plotly_max_balance(request):
    df = fetch_data_max_balance()

    fig = px.bar(df, x='ID', y='Max_Amount',
                 title="Max Money Used by Each User",
                 labels={"ID": "User ID", "Max_Amount": "Max Money Used"})

    fig.update_layout(
        xaxis_tickangle=-90,
        width=1200,
        height=500
    )

    # Return as an HTML response
    plot_html = fig.to_html(full_html=True)
    return HttpResponse(plot_html)


from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import os
import django
import pandas as pd
from django.db import connection
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
import plotly.express as px
from plotly.offline import plot

# Ініціалізація Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BANK.settings')  # Замініть на назву вашого проєкту
django.setup()


# Створення форми для введення User_ID
class UserIDForm(forms.Form):
    user_id = forms.IntegerField(label="Enter User ID", min_value=1)


# Функція для отримання даних балансу з бази
def fetch_data_balance(user_id):
    with connection.cursor() as cursor:
        cursor.execute("USE bank_2_dublicate;")
        cursor.execute("SET @Balance := (SELECT Money_Left FROM user WHERE ID = %s);", [user_id])


    query = """
        SELECT 
            o.Time_started,
            o.Money_Used,
            o.Operation_Type,
            (@Balance := CASE 
                WHEN o.Operation_Type = 'a' THEN @Balance - o.Money_Used 
                WHEN o.Operation_Type = 'w' THEN @Balance + o.Money_Used 
                ELSE @Balance 
            END) AS Balance_Before_Operation
        FROM 
            operation o
        WHERE 
            o.User_ID = %s
        ORDER BY 
            o.Time_started DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        rows = cursor.fetchall()

    columns = ['Time_started', 'Money_Used', 'Operation_Type', 'Balance_Before_Operation']
    df = pd.DataFrame(rows, columns=columns)

    # Перетворення колонок з Decimal в float
    df['Money_Used'] = df['Money_Used'].astype(float)
    df['Balance_Before_Operation'] = df['Balance_Before_Operation'].astype(float)

    return df


def plot_bokeh_balance(request):
    user_id = request.GET.get('user_id')  # Retrieve user_id from query parameters
    if not user_id:
        return HttpResponse("User ID is required.")

    df = fetch_data_balance(user_id)
    if df.empty:
        return HttpResponse("No data available for the given User ID.")

    # Generate Bokeh graph
    output_file(f"bokeh_balance_{user_id}.html")

    # Convert time to a format suitable for the graph
    df['Time_started'] = pd.to_datetime(df['Time_started'])
    source = ColumnDataSource(df)

    p = figure(title="Balance Over Time", x_axis_label="Time", y_axis_label="Balance Before Operation",
               x_axis_type='datetime', height=500, width=800)

    p.line(x='Time_started', y='Balance_Before_Operation', source=source, line_width=2, color="green", legend_label="Balance")

    p.legend.location = "top_left"
    p.legend.background_fill_color = "white"

    show(p)
    return HttpResponse(f"Bokeh graph for user {user_id} has been generated.")



# Функція для побудови графіка Plotly
def plot_plotly_balance(request):
    user_id = request.GET.get('user_id')  # Retrieve user_id from query parameters
    if not user_id:
        return HttpResponse("User ID is required.")

    df = fetch_data_balance(user_id)
    if df.empty:
        return HttpResponse("No data available for the given User ID.")

    # Generate Plotly graph
    fig = px.line(df, x='Time_started', y='Balance_Before_Operation',
                  title="Balance Over Time",
                  labels={"Time_started": "Time", "Balance_Before_Operation": "Balance"})

    fig.write_html(f"plotly_balance_{user_id}.html", auto_open=True)
    return HttpResponse(f"Plotly graph for user {user_id} has been generated.")


# View для відображення графіка
def user_balance_view(request):
    if request.method == 'POST':
        form = UserIDForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            # Redirect to the respective view for Bokeh or Plotly graph generation
            return redirect(f'/users/bokeh_balance/?user_id={user_id}')
    else:
        form = UserIDForm()

    return render(request, 'user_balance_form.html', {'form': form})

from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN
import plotly.express as px
from plotly.offline import plot

# Fetch data for operations summary
def fetch_data_operations_summary():
    query = """
        SELECT User_ID, COUNT(*) AS Total_Operations
        FROM operation
        GROUP BY User_ID
        HAVING COUNT(*) > 20;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    columns = ['User_ID', 'Total_Operations']
    return pd.DataFrame(rows, columns=columns)


# Fetch data for detailed operations
def fetch_data_detailed_operations():
    query = """
        SELECT u.ID AS User_ID, o.Money_Used, o.Operation_Type
        FROM user u
        JOIN operation o ON u.ID = o.User_ID
        JOIN employee e ON u.ID = e.ID;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    columns = ['User_ID', 'Money_Used', 'Operation_Type']
    return pd.DataFrame(rows, columns=columns)

# Your graph generation functions here (see above)
def bokeh_operations_summary(request):
    df = fetch_data_operations_summary()

    source = ColumnDataSource(df)

    p = figure(title="Total Operations per User (Bokeh)",
               x_axis_label="User ID", y_axis_label="Total Operations",
               height=500, width=1500, x_range=df['User_ID'].astype(str).tolist())

    p.vbar(x='User_ID', top='Total_Operations', width=0.5, source=source, legend_label="Total Operations", color="blue")
    p.xaxis.major_label_orientation = "vertical"
    p.legend.location = "top_left"
    p.legend.background_fill_color = "white"

    plot_html = file_html(p, CDN, "Operations Summary (Bokeh)")
    return HttpResponse(plot_html)
def plotly_operations_summary(request):
    df = fetch_data_operations_summary()

    fig = px.bar(df, x='User_ID', y='Total_Operations',
                 title="Total Operations per User (Plotly)",
                 labels={"User_ID": "User ID", "Total_Operations": "Total Operations"})

    fig.update_layout(
        xaxis_tickangle=-90,
        width=1200,
        height=500
    )

    plot_html = fig.to_html(full_html=True)
    return HttpResponse(plot_html)
def plotly_detailed_operations(request):
    df = fetch_data_detailed_operations()

    fig = px.bar(df, x='User_ID', y='Money_Used', color='Operation_Type',
                 title="Money Used per User by Operation Type (Plotly)",
                 labels={"User_ID": "User ID", "Money_Used": "Money Used"})

    fig.update_layout(
        xaxis_tickangle=-90,
        width=1200,
        height=500
    )

    plot_html = fig.to_html(full_html=True)
    return HttpResponse(plot_html)


def bokeh_detailed_operations(request):
    df = fetch_data_detailed_operations()

    if df.empty:
        return HttpResponse("No data available for detailed operations.")

    # Ensure that the data types are correct
    df['Money_Used'] = df['Money_Used'].astype(float)

    # Creating a ColumnDataSource for Bokeh
    source = ColumnDataSource(df)

    # Creating the Bokeh plot
    p = figure(
        title="Money Used per User by Operation Type (Bokeh)",
        x_axis_label="User ID",
        y_axis_label="Money Used",
        height=500, width=1500,
        x_range=df['User_ID'].astype(str).unique().tolist()  # Use unique values for x_range
    )

    # Bar chart: Money Used for each User
    p.vbar(x='User_ID', top='Money_Used', width=0.5, source=source, legend_label="Money Used", color="green")

    # Rotate x-axis labels for better readability
    p.xaxis.major_label_orientation = "vertical"

    # Add a legend and set its location
    p.legend.location = "top_left"
    p.legend.background_fill_color = "white"

    # Embed the plot in an HTML response
    plot_html = file_html(p, CDN, "Detailed Operations (Bokeh)")

    return HttpResponse(plot_html)


from django.http import HttpResponse
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import file_html
from bokeh.resources import CDN
import pandas as pd
from django.db import connection

from django.http import HttpResponse
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import file_html
from bokeh.resources import CDN
import pandas as pd
from django.db import connection


# Fetch data for users with balance above average
def fetch_data_above_average_balance():
    query = """
        SELECT u.ID AS User_ID, u.Money_Left
        FROM user u
        WHERE u.Money_Left > (SELECT AVG(Money_Left) FROM user)
        LIMIT 100;  -- Limit the results to the first 100 users
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    columns = ['User_ID', 'Money_Left']
    df = pd.DataFrame(rows, columns=columns)

    # Return the DataFrame
    return df

# Bokeh Line Chart: Users with Balance Above Average (Bokeh)
from decimal import Decimal


from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN
import pandas as pd
from decimal import Decimal

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN
import pandas as pd
from decimal import Decimal

def bokeh_above_average_balance(request):
    df = fetch_data_above_average_balance()

    # Convert 'Money_Left' to float for consistency in arithmetic operations
    df['Money_Left'] = df['Money_Left'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)

    # Calculate the average balance and convert it to float
    average_balance = float(df['Money_Left'].mean())  # Ensure this is a float

    # Assign a sequential index for User_ID to ensure no gaps in x positions
    df['User_Index'] = range(len(df))

    # Create ColumnDataSource for Bokeh
    source = ColumnDataSource(df)

    # Calculate y-axis maximum value for padding
    max_y = df['Money_Left'].max() + (df['Money_Left'].max() * 0.1)
    print(max_y);
    # Create figure for column chart
    p = figure(title="Users with Balance Above Average (Bokeh - Column)",
               x_axis_label="User Index", y_axis_label="Balance",
               height=500, width=1500, x_range=df['User_Index'].astype(str).tolist(),
               toolbar_location="above", tools="pan,box_zoom,reset,save",
               y_range=(average_balance, max_y))  # Set Y-axis range explicitly

    # Add column bars
    p.vbar(x='User_Index', top='Money_Left', width=0.8, source=source, legend_label="Balance",
           color="green", alpha=0.7)

    # Add hover tool for better interactivity
    hover = HoverTool()
    hover.tooltips = [("User ID", "@User_ID"), ("Balance", "@Money_Left")]
    p.add_tools(hover)

    # Customize appearance
    p.xaxis.major_label_orientation = "vertical"
    p.xaxis.axis_label_standoff = 12
    p.legend.location = "top_left"
    p.legend.background_fill_color = "white"
    p.grid.grid_line_alpha = 0.3
    p.background_fill_color = "#f5f5f5"

    # Generate HTML output for the plot
    plot_html = file_html(p, CDN, "Balance Above Average (Column Chart)")
    return HttpResponse(plot_html)



import plotly.express as px

import plotly.express as px

def plotly_above_average_balance(request):
    df = fetch_data_above_average_balance()

    # Create a Plotly bar chart with swapped axes (User_ID on y-axis, Money_Left on x-axis)
    fig = px.bar(df, x='Money_Left', y='User_ID',
                 title="Users with Balance Above Average (Plotly - Bar)",
                 labels={'Money_Left': 'Balance', 'User_ID': 'User ID'})

    # Customize layout for better presentation
    fig.update_layout(
        title_x=0.5,  # Center the title
        yaxis_title="Balance",
        xaxis_title="User ID",
        plot_bgcolor="rgba(0,0,0,0)",  # Set background to transparent
        bargap=0.2  # Space between bars
    )

    # Generate HTML output for the plot
    plot_html = fig.to_html(full_html=False)
    return HttpResponse(plot_html)


from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot


def move_data_to_operation_OLAP():
    query = """
        SELECT Money_Used, Time_Completed, Operation_Type, User_ID_id 
        FROM users_operation WHERE (YEAR(Time_Completed) < YEAR(NOW())) OR (YEAR(Time_Completed) = YEAR(NOW()) AND MONTH(Time_Completed) < MONTH(NOW()));;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    with connection.cursor() as cursor:
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO users_operation_OLAP (Money_Used, Time_Completed, Operation_Type, User_ID_id)
                VALUES (%s, %s, %s, %s);
            """, (
                row['Money_Used'],
                row['Time_Completed'],
                row['Operation_Type'],
                row['User_ID_id']
            ))
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users_operation WHERE (YEAR(Time_Completed) < YEAR(NOW())) OR (YEAR(Time_Completed) = YEAR(NOW()) AND MONTH(Time_Completed) < MONTH(NOW()));")

    return HttpResponse("Дані успішно переміщено в operation_OLAP та видалено з operation.")


from django.db import connection
from django.http import HttpResponse
import pandas as pd


def update_analytics_with_pandas():
    query = """
        SELECT 
            Time_Completed,
            Money_Used,
            User_ID_id 
        FROM users_operation;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    if not rows:
        return HttpResponse("Немає даних для оновлення аналітики.")
    df = pd.DataFrame(rows, columns=columns)
    df['Money_Used'] = pd.to_numeric(df['Money_Used'], errors='coerce')
    df['Time_Completed'] = pd.to_datetime(df['Time_Completed'])
    df['month_year'] = df['Time_Completed'].dt.to_period('M').astype(str)
    employee_df = pd.read_sql("SELECT ID FROM users_employee", connection)
    df['is_employee'] = df['User_ID_id'].isin(employee_df['ID']).astype(int)
    analytics_df = df.groupby('month_year').agg(
        total_spending=('Money_Used', 'sum'),
        employee_spending=('Money_Used', lambda x: x[df['is_employee'] == 1].sum()),
    ).reset_index()

    analytics_df['total_impact_from_employees'] = (
        analytics_df['employee_spending'] / analytics_df['total_spending']
    ).fillna(0)
    analytics_df['total_impact_from_users'] = 1 - analytics_df['total_impact_from_employees']
    with connection.cursor() as cursor:
        for _, row in analytics_df.iterrows():
            cursor.execute("""
                INSERT INTO users_analitics(month_year, total_spending, total_impact_from_employees, total_impact_from_users)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    total_spending = VALUES(total_spending),
                    total_impact_from_employees = VALUES(total_impact_from_employees),
                    total_impact_from_users = VALUES(total_impact_from_users);
            """, (
                row['month_year'],
                row['total_spending'],
                row['total_impact_from_employees'],
                row['total_impact_from_users']
            ))
            move_data_to_operation_OLAP()
    return HttpResponse("Таблиця Analitics успішно оновлена.")



def fetch_analytics_data():
    query = """
        SELECT 
            month_year, 
            total_spending, 
            total_impact_from_employees * total_spending, 
            total_impact_from_users * total_spending 
        FROM users_analitics
        ORDER BY STR_TO_DATE(CONCAT(month_year, '-01'), '%Y-%m-%d');
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    columns = ['month_year', 'total_spending', 'total_impact_from_employees', 'total_impact_from_users']
    df = pd.DataFrame(rows, columns=columns)
    return df


def analytics_chart(request):
    update_analytics_with_pandas()
    df = fetch_analytics_data()
    if df.empty:
        return HttpResponse("Немає доступних даних для відображення аналітики.")
    df['month_year'] = pd.to_datetime(df['month_year'], format='%Y-%m')
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['month_year'],
        y=df['total_spending'],
        mode='lines+markers',
        name='Total Spending',
        line=dict(color='green')
    ))

    fig.add_trace(go.Scatter(
        x=df['month_year'],
        y=df['total_impact_from_employees'],
        mode='lines+markers',
        name='Impact from Employees',
        line=dict(color='yellow')
    ))
    fig.add_trace(go.Scatter(
        x=df['month_year'],
        y=df['total_impact_from_users'],
        mode='lines+markers',
        name='Impact from Users',
        line=dict(color='red')
    ))
    fig.update_layout(
        title="Monthly Analytics Overview",
        xaxis_title="Month-Year",
        yaxis_title="Amount",
        legend_title="Metrics",
        template="plotly_white"
    )
    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

    return render(request, 'myapp/analytics_chart.html', {'plot_div': plot_div})


def process_data(request):
    move_data_to_operation_OLAP()
    update_analytics_with_pandas()
    return HttpResponse("Дані успішно перенесено та аналітику оновлено.")