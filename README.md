# Image-E-Shop
An Image E-Shop created to buy images

The project was designed for the Fall 2022 Shopify Data Engineer Intern Challenge Question:
https://docs.google.com/document/d/1ijXrqQMOORukOWCWcwwcpxPcF_TczwvNE0wB4M2Orqg/edit#heading=h.n7bww7g70ipk


# How To Access Image E-Shop

You will need to install sqlite3 
```python
pip install pysqlite3 
```
And also install Flask
```python
pip install flask 
```

Once you have clones this repo (or downloaded all of the files to your local computer) simply cd into the folder where these program files are stored and run
```python
python3 imageRepo.py 
```

You will then see a pop-up similar to:
![image](https://user-images.githubusercontent.com/68351986/165835228-27f00ad3-6402-4f71-873b-e9810ca7a67a.png)

Then load the following website in your browser:
http://127.0.0.1:5000/

You will see the following website:

![image](https://user-images.githubusercontent.com/68351986/165836175-608141f3-d8e7-40a2-8671-6947ed53b84e.png)


# How to Use Image E-Shop

Using the Buy button, you can buy a certain image and continue to buy that item until the quantity runs out (in which the product will automatically be removed from the database)

You can also see the total amount you have bought and how many products are still in stock:

![image](https://user-images.githubusercontent.com/68351986/165836582-f5b7143e-dd72-47fc-b3c3-472444afb019.png)


Then you can access 'Sellers Dashboard' in order to see all of the sellers and the total profits they have made on x amount of products they have sold!

![image](https://user-images.githubusercontent.com/68351986/165836724-58e07759-c9be-4e26-a2b7-6a91e4ad3474.png)


Click 'Main page' to return back to the Homepage and 'Reset Database' to reset the database!

# Testing

I used PyTest in order to test the Flask app that was built on Python and SQLite3

# Future Implementations
In terms of architecture, I have designed a two-tier architecture which, in the future, I would like to implement a three-tier architecture for better security and sustainability of the database on the website. In addition, I would like to implement a login feature in order to track each seller/buyer and allow different users to also sell items in the website. This would be an efficient implemntation that would consist of a few more post and get methods along with writing a few more SQL queries by joining different tables.


