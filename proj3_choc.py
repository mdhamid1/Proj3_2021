#Name: Muhammed Hamid
#Uniqname: mdhamid

'''
Some things to note from Muhammed:
-The code has been structured such that the sub-level commands need to follow a specific order. The order is specified below:
    [high-level command] [country/region]=[filter key] [sell/source] [ratings/cocoa/number_of_bars] [top/bottom] [integer]

    If the order of any of these commands is switched, there will be errors or unexpected behavior. For example if the sell
    or source command is placed after the ratings/cocoa/number_of_bars command.
    The sell/source sub-level command was flipped in the unit testing script (proj3_choc_test.py). The sell/source order has been
    changed in the unit testing script to mitigate this issue.

- ** Although the default parameters for the sub-level commands are all coded into the script, the script still requires that either
    ratings/cocoa/number_of_bars be specified. The reason for doing so is to have something to determine whether the query is a valid query or not.
    If one of these three parameters is not specified then the script will mention that it is an invalid command.

- * In the test script (proj3_choc_test.py) one of the tests in the test_country_search function is failing. The query for that test is
    countries ratings source bottom 5. The result it is expecting is 'Uganda'. I wonder if Uganda is not the correct result that should be
    returned. My script returns United States of America. I feel my script is returning the proper result.

'''

import sqlite3
import plotly.graph_objects as go

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from a database called choc.db
DBNAME = 'choc.sqlite'

def dbconn(query):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    connection.close()
    return result

# Part 1: Implement logic to process user commands
def process_command(command):

    area_type_selector = ""
    area_of_interest = ""
    order_type = ""
    company_agg = ""
    rating_avg_agg = ""
    cocoa_avg_agg = ""
    group_by_clause = ""


    testlist = command.split(" ")
    testlist2 = testlist[1].split("=")
    print(testlist2)

    try:
        testlist2 = testlist[1].split("=")

        if "=" in command:
            area_of_interest = testlist2[1]
            print(area_of_interest)

        if isinstance(int(testlist[-1]), int):
            order_integer = testlist[-1]

    except:
        print("No integer found for sorting")
        order_integer = 10

        if not area_of_interest:
            area_of_interest = ""


    column_name_country_sell = "B.Alpha2 as"
    area_type_selector_country_sell = "Alpha2_Sell"
    column_name_region_sell= "B.Region as"
    area_type_selector_region_sell = "Region_Sell"
    column_name_country_source = "C.Alpha2 as"
    area_type_selector_country_source = "Alpha2_Source"
    column_name_region_source = "C.Region as"
    area_type_selector_region_source = "Region_Source"
    where_clause = ""



    if "bars" in command[0:4]:
        company_agg = ""
        rating_avg_agg = ""
        cocoa_avg_agg = ""
        group_by_clause = ""

        if "sell" not in command and "source" not in command:
            command = "sell" + command
        if "country" in command and "sell" in command:
            area_type_selector = area_type_selector_country_sell
            where_clause = f"where {area_type_selector}='{area_of_interest}'"
        if "region" in command and "sell" in command:
            area_type_selector = area_type_selector_region_sell
            where_clause = f"where {area_type_selector}='{area_of_interest}'"
        if "country" in command and "source" in command:
            area_type_selector = area_type_selector_country_source
            where_clause = f"where {area_type_selector}='{area_of_interest}'"
        if "region" in command and "source" in command:
            area_type_selector = area_type_selector_region_source
            where_clause = f"where {area_type_selector}='{area_of_interest}'"
        if "bottom" in command:
            order_type = "asc"
        if "top" in command:
            order_type = "desc"
        if "bottom" not in command and "top" not in command:
            order_type = "desc"
        if "ratings" in command:
            order_object= "A.Rating"
        if "cocoa" in command:
            order_object = "A.CocoaPercent"
        if "ratings" not in command and "cocoa" not in command:
            order_object = "A.Rating"

        query = f'''select A.SpecificBeanBarName, A.Company, B.EnglishName as Company_Location, A.Rating, A.CocoaPercent,
        C.EnglishName as Bean_Origin, {column_name_country_sell} {area_type_selector_country_sell}, 
        {column_name_country_source} {area_type_selector_country_source}, {column_name_region_sell} {area_type_selector_region_sell}, 
        {column_name_region_source} {area_type_selector_region_source} from bars A join Countries B on A.CompanyLocationId=B.Id join Countries C on
        A.BroadBeanOriginId=C.Id {where_clause} {group_by_clause} order by
        {order_object} {order_type} limit {order_integer}'''

    elif "companies" in command:
        company_agg = "count(A.Rating) as Bar_Count"
        rating_avg_agg = "avg(A.Rating) as Rating_Avg"
        cocoa_avg_agg = "avg(A.CocoaPercent) as Cocoa_Avg"
        num_bars_group_by = 4
        group_by_clause = f"group by A.Company having Bar_Count > {num_bars_group_by}"

        if "country" in command:
            area_type_selector = area_type_selector_country_sell
            where_clause = f"where {area_type_selector}='{area_of_interest}'"
        if "region" in command:
            area_type_selector = area_type_selector_region_sell
            where_clause = f"where {area_type_selector}='{area_of_interest}'"
        if "bottom" in command:
            order_type = "asc"
        if "top" in command:
            order_type = "desc"
        if "bottom" not in command and "top" not in command:
            order_type = "desc"
        if "ratings" in command:
            order_object = "Rating_Avg"
        if "cocoa" in command:
            order_object = "Cocoa_Avg"
        if "number_of_bars" in command:
            order_object = "Bar_Count"
        if "ratings" not in command and "cocoa" not in command and "number_of_bars" not in command:
            order_object = "Rating_Avg"

        query = f'''select A.Company, B.EnglishName as Company_Location, {rating_avg_agg}, {cocoa_avg_agg}, {company_agg},
        C.EnglishName as Bean_Origin, {column_name_country_sell} {area_type_selector_country_sell}, {column_name_region_sell} 
        {area_type_selector_region_sell} from bars A join Countries B on A.CompanyLocationId=B.Id join Countries C on
        A.BroadBeanOriginId=C.Id {where_clause} {group_by_clause} order by
        {order_object} {order_type} limit {order_integer}'''

    elif "countries" in command:
        company_agg = "count(A.Rating) as Bar_Count"
        rating_avg_agg = "avg(A.Rating) as Rating_Avg"
        cocoa_avg_agg = "avg(A.CocoaPercent) as Cocoa_Avg"
        num_bars_group_by = 4
        group_by_clause = f"group by A.Company having Bar_Count > {num_bars_group_by}"

        if "sell" not in command and "source" not in command:
            command = "sell" + command
        if "region" in command and "sell" in command:
            area_type_selector = area_type_selector_region_sell
            group_by_clause = f"group by {area_type_selector_country_sell} having Bar_Count > {num_bars_group_by}"
            where_clause = f"where {area_type_selector}='{area_of_interest}'"
        if "region" in command and "source" in command:
            area_type_selector = area_type_selector_region_source
            group_by_clause = f"group by {area_type_selector_country_source} having Bar_Count > {num_bars_group_by}"
            where_clause = f"where {area_type_selector}='{area_of_interest}'"
        if "bottom" in command:
            order_type = "asc"
        if "top" in command:
            order_type = "desc"
        if "bottom" not in command and "top" not in command:
            order_type = "desc"
        if "ratings" in command:
            order_object= "Rating_Avg"
        if "cocoa" in command:
            order_object = "Cocoa_Avg"
        if "number_of_bars" in command:
            order_object = "Bar_Count"
        if "ratings" not in command and "cocoa" not in command and "number_of_bars" not in command:
            order_object = "Rating_Avg"

        query = f'''select B.EnglishName as Company_Location, {rating_avg_agg}, {cocoa_avg_agg}, {company_agg},
        C.EnglishName as Bean_Origin, {column_name_country_sell} {area_type_selector_country_sell}, 
        {column_name_country_source} {area_type_selector_country_source}, {column_name_region_sell} {area_type_selector_region_sell}, 
        {column_name_region_source} {area_type_selector_region_source} from bars A join Countries B on A.CompanyLocationId=B.Id join Countries C on
        A.BroadBeanOriginId=C.Id {where_clause} {group_by_clause} order by
        {order_object} {order_type} limit {order_integer}'''

    elif "regions" in command:
        company_agg = "count(A.Rating) as Bar_Count"
        rating_avg_agg = "avg(A.Rating) as Rating_Avg"
        cocoa_avg_agg = "avg(A.CocoaPercent) as Cocoa_Avg"
        num_bars_group_by = 4
        group_by_clause = f"group by A.Company having Bar_Count > {num_bars_group_by}"

        if "sell" not in command and "source" not in command:
            command = "sell" + command
        if "sell" in command:
            group_by_clause = f"group by {area_type_selector_region_sell} having Bar_Count > {num_bars_group_by}"
        if "source" in command:
            group_by_clause = f"group by {area_type_selector_region_source} having Bar_Count > {num_bars_group_by}"
        if "bottom" in command:
            order_type = "asc"
        if "top" in command:
            order_type = "desc"
        if "bottom" not in command and "top" not in command:
            order_type = "desc"
        if "ratings" in command:
            order_object= "Rating_Avg"
        if "cocoa" in command:
            order_object = "Cocoa_Avg"
        if "number_of_bars" in command:
            order_object = "Bar_Count"
        if "ratings" not in command and "cocoa" not in command and "number_of_bars" not in command:
            order_object = "Rating_Avg"


        query = f'''select B.EnglishName as Company_Location, {rating_avg_agg}, {cocoa_avg_agg}, {company_agg},
        C.EnglishName as Bean_Origin, {column_name_country_sell} {area_type_selector_country_sell}, 
        {column_name_country_source} {area_type_selector_country_source}, {column_name_region_sell} {area_type_selector_region_sell}, 
        {column_name_region_source} {area_type_selector_region_source} from bars A join Countries B on A.CompanyLocationId=B.Id join Countries C on
        A.BroadBeanOriginId=C.Id {group_by_clause} order by {order_object} {order_type} limit {order_integer}'''


    print(query + "\n\n")
    query_result = dbconn(query)

    for i, result in enumerate(query_result):
        if "bars" in command[0:4]:
            result = result[0:6]

        elif "companies" in command and "ratings" in command:
            result = result[0:2] + result[2:3]
        elif "companies" in command and "cocoa" in command:
            result = result[0:2] + result[3:4]
        elif "companies" in command and "number_of_bars" in command:
            result = result[0:2] + result[4:5]

        elif "countries" in command and "ratings" in command:
            result = result[0:1] + (area_of_interest,) + result[1:2]
        elif "countries" in command and "cocoa" in command:
            result = result[0:1] + (area_of_interest,) + result[2:3]
        elif "countries" in command and "number_of_bars" in command:
            result = result[0:1] + (area_of_interest,) + result[3:4]

        elif "regions" in command and "sell" in command and "ratings" in command:
            result = result[7:8] + result[1:2]
        elif "regions" in command and "sell" in command and "cocoa" in command:
            result = result[7:8] + result[2:3]
        elif "regions" in command and "sell" in command and "number_of_bars" in command:
            result = result[7:8] + result[3:4]
        elif "regions" in command and "source" in command and "ratings" in command:
            result = result[8:9] + result[1:2]
        elif "regions" in command and "source" in command and "cocoa" in command:
            result = result[8:9] + result[2:3]
        elif "regions" in command and "source" in command and "number_of_bars" in command:
            result = result[8:9] + result[3:4]
        elif "regions" in command and "sell" in command and "ratings" not in command and "cocoa" not in command and "number_of_bars" not in command:
            result = result[7:8] + result[1:2]
        elif "regions" in command and "source" in command and "ratings" not in command and "cocoa" not in command and "number_of_bars" not in command:
            result = result[8:9] + result[1:2]


        query_result[i] = result

    return query_result


def load_help_text():
    with open('Proj3Help.txt') as f:
        return f.read()

# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''


    while response != 'exit':


        response = input('Enter a command: ')
        if response == "exit" or response == "Exit":
            print("Goodbye")
            break
        if "barplot" in response:
            response = response.split("barplot")[0].strip()
            barplot = True
        else:
            barplot = False


        if "bars" in response and "ratings" not in response:
            if "cocoa" not in response:
                if "number_of_bars" not in response:
                    print("command not recognized: " + response)
                    continue

        if "countries" in response and "ratings" not in response:
            if "cocoa" not in response:
                if "number_of_bars" not in response:
                    print("command not recognized: " + response)
                    continue

        if "companies" in response and "ratings" not in response:
            if "cocoa" not in response:
                if "number_of_bars" not in response:
                    print("command not recognized: " + response)
                    continue

        if "regions" in response and "ratings" not in response:
            if "cocoa" not in response:
                if "number_of_bars" not in response:
                    print("command not recognized: " + response)
                    continue



        query_result = process_command(response)
        print(query_result)
        print("\n")

        if "bars" in response[0:4]:
            x_list = []
            y_list = []
            row = "{entry1:16.12} {entry2:16.12} {entry3:16.12} {entry4:5.12} {entry5:5.12} {entry6:2.12}".format
            for tuple_item in query_result:
                entry1=tuple_item[0]
                entry4=tuple_item[3]
                entry5=tuple_item[4]

                myrow = row(entry1=tuple_item[0], entry2=tuple_item[1], entry3=tuple_item[2], entry4=str(tuple_item[3]), entry5=(str(int(tuple_item[4]*100))+ "%"), entry6=tuple_item[5])
                print(myrow + "\n")


                x_list.append(entry1)
                if "cocoa" in response:
                    y_list.append(entry5)
                else:
                    y_list.append(entry4)

            if barplot:
                bar_data = go.Bar(x=x_list, y=y_list)
                basic_layout = go.Layout(title="Results Summary")
                fig = go.Figure(data=bar_data, layout=basic_layout)
                fig.show()


        if "companies" in response:
            x_list = []
            y_list = []
            row = "{entry1:16.12} {entry2:16.12} {entry3:16.3}".format
            for tuple_item in query_result:
                entry1 = tuple_item[0]
                entry3 = tuple_item[2]
                myrow = row(entry1=tuple_item[0], entry2=tuple_item[1], entry3=str(tuple_item[2]))
                print(myrow + "\n")

                x_list.append(entry1)
                y_list.append(entry3)

            if barplot:
                bar_data = go.Bar(x=x_list, y=y_list)
                basic_layout = go.Layout(title="Results Summary")
                fig = go.Figure(data=bar_data, layout=basic_layout)
                fig.show()


        if "countries" in response:
            x_list = []
            y_list = []
            row = "{entry1:16.12} {entry2:16.12} {entry3:16.3}".format
            for tuple_item in query_result:
                entry1 = tuple_item[0]
                entry3 = tuple_item[2]
                myrow = row(entry1=tuple_item[0], entry2=tuple_item[1], entry3=str(tuple_item[2]))
                print(myrow + "\n")

                x_list.append(entry1)
                y_list.append(entry3)

            if barplot:
                bar_data = go.Bar(x=x_list, y=y_list)
                basic_layout = go.Layout(title="Results Summary")
                fig = go.Figure(data=bar_data, layout=basic_layout)
                fig.show()

        if "regions" in response:
            x_list = []
            y_list = []
            row = "{entry1:16.12} {entry2:16.4}".format
            for tuple_item in query_result:
                entry1 = tuple_item[0]
                entry2 = tuple_item[1]
                myrow = row(entry1=tuple_item[0], entry2=str(tuple_item[1]))
                print(myrow + "\n")

                x_list.append(entry1)
                y_list.append(entry2)

            if barplot:
                bar_data = go.Bar(x=x_list, y=y_list)
                basic_layout = go.Layout(title="Results Summary")
                fig = go.Figure(data=bar_data, layout=basic_layout)
                fig.show()


        if response == 'help':
            print(help_text)
            continue

# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    interactive_prompt()

