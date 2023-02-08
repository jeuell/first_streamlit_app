
import streamlit as sl
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

sl.title("My Mom's Healthy Diner")
sl.header('Breakfast Favorites')
sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinach & Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')
   
sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# sl.dataframe(my_fruit_list)
sl.dataframe(fruits_to_show)

# Display the table on the page.

# New Section to display fruityvice api response

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get ("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   fruityvice_normalized = pd.json_normalize(fruityvice_response.json ())
   return fruityvice_normalized

sl.header('Fruityvice Fruit Advice!')
try:
   fruit_choice = sl.text_input('What fruit would you like information about?')
   if not fruit_choice:
      sl.error("Please select a fruit to get information.")
   else:
      sl.dataframe(get_fruityvice_data('kiwi'))
                                
except URLError as e:
   sl.error ()


sl.header ("The fruit load list contains:") 
#Snowflake-related functions
def get_fruit_load_list(my_cnx):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from fruit load list")
      return my_cur.fetchall()

# Add a button to load the fruit
if sl.button ('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
   my_data_rows = get_fruit_load_list(my_cnx)
   sl.dataframe(my_data_rows)
                                                         
# don't run anything past here while we troubleshoot
sl.stop()


# my_cnx = sf.connector.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
#sl.text("Hello from Snowflake:")
sl.header("My fruit list contains:")
sl.dataframe(my_data_rows)

add_my_fruit = sl.text_input('What fruit would you like to add?','Jackfruit')
sl.write('Thanks for adding ', add_my_fruit)

#This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
