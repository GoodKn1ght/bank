import os
import django
import pandas as pd
from django.db import connection
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
import plotly.express as px

# Ініціалізація Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BANK.settings')  # Замініть на назву вашого проєкту
django.setup()

# Виконання SQL-запиту для отримання максимального використаного балансу по кожному користувачеві
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

    columns = [desc[0] for desc in cursor.description]  # Отримуємо імена колонок
    df = pd.DataFrame(rows, columns=columns)

    # Перетворюємо Max_Amount на тип float для коректного відображення на графіку
    df['Max_Amount'] = df['Max_Amount'].astype(float)

    return df


# Побудова графіка Bokeh для максимального використаного балансу (лінійний графік)
def plot_bokeh_max_balance(df):
    output_file("bokeh_max_balance_line.html")

    # Перетворюємо дані для лінійного графіку
    df['ID'] = df['ID'].astype(str)  # Переконуємось, що значення на осі X - рядкові

    source = ColumnDataSource(df)

    p = figure(title="Max Money Used by Each User",
               x_axis_label="User ID", y_axis_label="Max Money Used",
               height=500, width=1500, x_range=df['ID'].tolist())  # Збільшена ширина для підписів

    p.line(x='ID', y='Max_Amount', source=source, line_width=2, color="orange", legend_label="Max Amount")

    p.xaxis.major_label_orientation = "vertical"  # Повертаємо підписи по осі X вертикально
    p.legend.location = "top_left"
    p.legend.background_fill_color = "white"

    print("Відкриваю лінійний графік Bokeh для Max Balance...")
    show(p)


# Побудова графіка Plotly для максимального використаного балансу
def plot_plotly_max_balance(df):
    fig = px.bar(df, x='ID', y='Max_Amount',
                 title="Max Money Used by Each User",
                 labels={"ID": "User ID", "Max_Amount": "Max Money Used"})

    fig.update_layout(
        xaxis_tickangle=-90,  # Поворот підписів по осі X на 90 градусів
        width=1200,  # Збільшена ширина
        height=500,  # Встановлено висоту для кращого вигляду

    yaxis = dict(range=[4988, 5000])  # Встановлення початкового значення для осі Y
    )

    fig.write_html("plotly_max_balance.html", auto_open=True)
    print("Графік Plotly збережено у файл і відкрито у браузері...")


# Основна функція
if __name__ == "__main__":
    # Отримуємо дані для максимального використаного балансу
    df_max_balance = fetch_data_max_balance()

    if df_max_balance.empty:
        print("No data available for max balance users.")
    else:
        print("Data fetched successfully for max balance users:")
        print(df_max_balance)

        # Побудова графіків для максимального використаного балансу
        print("Displaying Bokeh line chart for max balance...")
        plot_bokeh_max_balance(df_max_balance)

        print("Displaying Plotly chart for max balance...")
        plot_plotly_max_balance(df_max_balance)
        import os
        import django
        import pandas as pd
        from django.db import connection
        import plotly.express as px

        # Ініціалізація Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BANK.settings')  # Замініть на назву вашого проєкту
        django.setup()


        # Виконання SQL-запиту для отримання користувачів із залишком більше середнього, обмежених 1000 записами
        def fetch_data_average_balance():
            query = """
                SELECT u.ID, 
                       (SELECT AVG(Money_Left) FROM user) AS Average_Money_Left
                FROM user u
                WHERE u.Money_Left > (SELECT AVG(Money_Left) FROM user)
                LIMIT 10;
            """


            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]  # Отримуємо імена колонок
            df = pd.DataFrame(rows, columns=columns)

            # Перетворюємо Average_Money_Left на тип float для коректного відображення на графіку
            df['Average_Money_Left'] = df['Average_Money_Left'].astype(float)

            return df


        # Побудова графіка Plotly для користувачів із залишком більше середнього
        def plot_plotly_average_balance(df):
            fig = px.bar(df, x='ID', y='Average_Money_Left',
                         title="Money Left for Users Above Average",
                         labels={"ID": "User ID", "Average_Money_Left": "Money Left"})
            # Зміна мінімального значення осі Y на середнє значення
            min_y = df['Average_Money_Left'].min()
            max_y = df['Average_Money_Left'].max()
            fig.update_layout(
                xaxis_tickangle=-45,  # Окружаємо підписи по осі X під кутом
                yaxis=dict(range=[min_y, max_y]),  # Задаємо діапазон осі Y
                width=1200,  # Збільшена ширина
                height=500  # Встановлено висоту для кращого вигляду
            )

            fig.write_html("plotly_average_balance.html", auto_open=True)
            print("Графік Plotly збережено у файл і відкрито у браузері...")


        # Основна функція
        if __name__ == "__main__":
            # Отримуємо дані для користувачів із залишком більше середнього (обмежено 1000 записами)
            df_average_balance = fetch_data_average_balance()

            if df_average_balance.empty:
                print("No data available for users with balance above average.")
            else:
                print("Data fetched successfully for users with balance above average:")
                print(df_average_balance)

                print("Displaying Plotly chart for average balance...")
                plot_plotly_average_balance(df_average_balance)
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


        # Функція для виконання SQL-запитів
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


        # Побудова графіків Bokeh
        def plot_bokeh_summary(df):
            output_file("bokeh_summary.html")
            source = ColumnDataSource(df)
            p = figure(x_range=df['User_ID'].astype(str), title="Total Operations per User",
                       x_axis_label="User ID", y_axis_label="Total Operations", height=600)
            p.vbar(x='User_ID', top='Total_Operations', width=0.5, source=source, color="navy", alpha=0.7)
            print("Відкриваю графік Bokeh для Total Operations...")
            show(p)


        def plot_bokeh_detailed(df):
            output_file("bokeh_detailed.html")
            df_a = df[df['Operation_Type'] == 'a']
            df_w = df[df['Operation_Type'] == 'w']
            p = figure(title="Operations by User", x_axis_label="Money Used", y_axis_label="User ID", height=600)
            p.line(df_a['Money_Used'], df_a['User_ID'], color="green", legend_label="Operation Type: a", line_width=2)
            p.line(df_w['Money_Used'], df_w['User_ID'], color="red", legend_label="Operation Type: w", line_width=2)
            p.legend.title = "Operation Types"
            p.legend.location = "top_left"
            p.legend.background_fill_color = "white"
            print("Відкриваю графік Bokeh для детальних операцій...")
            show(p)


        def plot_bokeh_office_summary(df):
            output_file("../templates/myapp/bokeh_office_summary.html")
            source = ColumnDataSource(df)

            # Визначаємо ширину графіка динамічно, залежно від кількості офісів
            plot_width = max(800, len(df['Office']) * 100)

            p = figure(x_range=df['Office'], title="Employee Count per Office",
                       x_axis_label="Office", y_axis_label="Employee Count",
                       height=500, width=plot_width)

            # Налаштовуємо стовпчики
            p.vbar(x='Office', top='Employee_Count', width=0.5, source=source, color="blue", alpha=0.7)

            # Налаштовуємо відображення підписів осей
            p.xaxis.major_label_orientation = 1.2  # Повертаємо підписи осі X
            p.xgrid.grid_line_color = None  # Прибираємо вертикальні сітки

            print("Відкриваю графік Bokeh для Office Summary...")
            show(p)


        # Побудова графіків Plotly
        def plot_plotly_summary(df):
            fig = px.line(df, x='User_ID', y='Total_Operations',
                          title="Total Operations per User",
                          labels={"User_ID": "User ID", "Total_Operations": "Total Operations"})
            plot(fig, filename="plotly_summary.html", auto_open=True)
            print("Графік Plotly для Total Operations збережено у файл і відкрито у браузері...")


        def plot_plotly_detailed(df):
            color_map = {'a': 'green', 'w': 'red'}
            df['Color'] = df['Operation_Type'].map(color_map)
            fig = px.scatter(df, x='Money_Used', y='User_ID', color='Operation_Type',
                             color_discrete_map=color_map,
                             title="Operations by User (Detailed)",
                             labels={"User_ID": "User ID", "Money_Used": "Money Used"})
            fig.write_html("plotly_detailed.html", auto_open=True)
            print("Графік Plotly для детальних операцій збережено у файл і відкрито у браузері...")


        def plot_plotly_office_summary(df):
            fig = px.bar(df, x='Office', y='Employee_Count',
                         title="Employee Count per Office",
                         labels={"Office": "Office", "Employee_Count": "Employee Count"},
                         color='Employee_Count', color_continuous_scale="Viridis")
            fig.write_html("plotly_office_summary.html", auto_open=True)
            print("Графік Plotly для Office Summary збережено у файл і відкрито у браузері...")


        # Основна функція
        if __name__ == "__main__":
            # Дані для першого запиту
            df_summary = fetch_data_operations_summary()
            if not df_summary.empty:
                plot_bokeh_summary(df_summary)
                plot_plotly_summary(df_summary)

            # Дані для другого запиту
            df_detailed = fetch_data_detailed_operations()
            if not df_detailed.empty:
                plot_bokeh_detailed(df_detailed)
                plot_plotly_detailed(df_detailed)
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


        # Виконання SQL-запиту для отримання даних із балансом
        def fetch_data_balance():
            # Виконуємо перший запит SET
            with connection.cursor() as cursor:
                cursor.execute("USE bank_2_dublicate;")
                cursor.execute("SET @Balance := (SELECT Money_Left FROM user WHERE ID = 2);")

            # Виконуємо основний запит для отримання даних
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
                    o.User_ID = 2
                ORDER BY 
                    o.Time_started DESC;
            """

            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            columns = ['Time_started', 'Money_Used', 'Operation_Type', 'Balance_Before_Operation']
            df = pd.DataFrame(rows, columns=columns)

            # Перетворення колонок з Decimal в float
            df['Money_Used'] = df['Money_Used'].astype(float)
            df['Balance_Before_Operation'] = df['Balance_Before_Operation'].astype(float)

            return df


        # Побудова графіка Bokeh для балансу
        def plot_bokeh_balance(df):
            output_file("bokeh_balance.html")

            # Перетворюємо час на формат, зручний для графіка
            df['Time_started'] = pd.to_datetime(df['Time_started'])

            source = ColumnDataSource(df)

            p = figure(title="Balance Over Time", x_axis_label="Time", y_axis_label="Balance Before Operation",
                       x_axis_type='datetime', height=500, width=800)

            p.line(x='Time_started', y='Balance_Before_Operation', source=source, line_width=2, color="green",
                   legend_label="Balance")

            p.legend.location = "top_left"
            p.legend.background_fill_color = "white"

            print("Відкриваю графік Bokeh для Balance...")
            show(p)


        # Побудова графіка Plotly для балансу
        def plot_plotly_balance(df):
            # Перетворюємо час на формат, зручний для графіка
            df['Time_started'] = pd.to_datetime(df['Time_started'])

            fig = px.line(df, x='Time_started', y='Balance_Before_Operation',
                          title="Balance Over Time",
                          labels={"Time_started": "Time", "Balance_Before_Operation": "Balance"})

            fig.write_html("plotly_balance.html", auto_open=True)
            print("Графік Plotly збережено у файл і відкрито у браузері...")


        # Основна функція
        if __name__ == "__main__":
            # Отримуємо дані для балансу
            df_balance = fetch_data_balance()


            if df_balance.empty:
                print("No data available for balance.")
            else:
                print("Data fetched successfully for balance:")
                print(df_balance)

                # Побудова графіків для балансу
                print("Displaying Bokeh chart for balance...")
                plot_bokeh_balance(df_balance)

                print("Displaying Plotly chart for balance...")
                plot_plotly_balance(df_balance)

            # Отримуємо дані для кількості працівників по офісах
            df_office = fetch_data_office_summary()

            if df_office.empty:
                print("No data available for office summary.")
            else:
                print("Data fetched successfully for office summary:")
                print(df_office)

                # Побудова графіків для кількості працівників по офісах
                print("Displaying Bokeh chart for office summary...")
                plot_bokeh_office_summary(df_office)

                print("Displaying Plotly chart for office summary...")
                plot_plotly_office_summary(df_office)

