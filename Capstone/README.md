## Documentation

This is a capstone project for CS50’s Web Programming with Python and JavaScript. The web application is a hotel webpage, named Tsilal. I have previously built a page using PHP and a database using phpMyAdmin. And this time, I want to expose myself building a similar page using the programming languages I have developed from this course. Moreover, I am convinced that I can add enough difficulty compared to prior projects and I have made sure that it is distinct from previous projects in the course. Here, I have designed the front-end using HTML, CSS, and JavaScript. While for the back-end, as part of the requirement, I have used Python using Django framework. JSON is used to structurally transmit data between the front-end and back-end. 

## Specifications

- *Index:* This is the landing page when a user is initially logged in.
	- *From and To:* The From and To fields should only allow a reasonable date. In addition, once they are submitted and other fields are displayed, the From and To fields should be disabled.
	- *Price:* The total price changes accordingly when the user chooses a room.
- *Reservation:* Instead of directly booking a room a user can also reserve a room. 
	- *Page:* Once reserved the user can check the reservation on a separate page. And it will be made sure that only one reservation is allowed, and the user is informed about the existing reservation if another reservation is tried to be made.
	- *Book/Cancel:* The reservation can be cancelled or booked while the reservation is available. In both cases, the reservation will be deleted.
- *Expired reservation:* Any reservation should be available for 24 hours before expiry. A timer indicates the time left until the reservation expires. 
- *Bookings:* A user after filling all the fields can book a room. 
- All the users’ bookings will be displayed in a separate page.
- *Email booking:* An email will be sent to the user’s address with all the necessary details of the booking.
- *Mobile-responsiveness:* The site should be responsive to accommodate mobile-responsiveness. A 400x865 dimension mobile phone can be considered while making it responsive.
	- *Background:* A different (probably portrait) image will be displayed.
	- *Scroll:* When the page overflow in any direction, the page should allow scrolling.
	- *Navigation:* The page should only display the navigation options after clicking a hamburger menu.
- *Non-existing / Not-authenticated page:* 
	- *404 Page (Unauthorized/Does Not Exist):* Display an appropriate page for a page that does not exist or if an authenticated user tries to access a page.
- *Models:* The models used can be displayed via the admin page. And the admin should be given the right to add room types along with their prices.

## Project Files description

*/settings.py*
All the code is auto generated during the project creating though the Django framework. Some global variables/identifiers are added as per the Django email system requirement.

*/hotel/views.py*
A list of all the functions called after requesting a GET, POST, or PUT methods. @csrf_exempt and/or @login_required are two decorators used for some functions to keep the integrity of submitted fields and authenticity of users. And there are some helper functions that facilitate the proper usage of the webpage.

*/hotel/models.py*
Five models are created here. They are User, Room, Reservation, Booking, and “RoomTypePrice”.

*/hotel/admin.py*
The models created are registered for their database to be accessed by the admin.

*/hotel/templates/layout.html*
This is the general layout page so that other HTML pages can extend it and implement page specific requirements.

*/hotel/static/layout.js*
A JavaScript helper file for the “layout.html” and handles on-content-load features that are to be extended by all other HTML files.

*/hotel/templates/index.html*
The initial landing page of the site. It displays varyingly whether users are logged in or not. 

*/hotel/static/index.js*
Functions so that “index.html” behaves in a natural way are implemented here. 

*/hotel/templates/reservation.html*
A page that displays a user’s reservation. The timer until the reservation expires is here. 
This page shows a no-reservation message if accessed by a user who does not have any reservation. 

*/hotel/static/reservation.js*
Event listeners to handle the timer of the reservation, and helpers for the “reservation.html” file rests here.

*/hotel/templates/booking.html*
A tabular view of all the user’s booking is here. Only bookings after the current date are displayed.

*/hotel/templates/login.html*
Users can login to the webpage through this page.

*/hotel/templates/register.html*
New users can create an account here.

*/hotel/templates/doesntexist.html*
A page that displays an error message when a broken link, non-existing page, or not-accessible page is visited.

*/hotel/static/styles.css*
All the styling and formatting of all the html files can be found from here. In addition, styling to make it mobile responsive are also developed here. 

## Distinctiveness and Complexity

The webpage is developed to meet a level of complexity which outweighs the prior projects. Being a hotel webpage ‘time’ is incorporated carefully inside. This is shown, for example, when users make a reservation. 24 hours is given to book the reservation, where a timer displays the time left until their reservation expires. JSON is used here, to fulfil the order to delete the reservation, from JavaScript to Django/Python. In addition, making the page mobile-responsive is an additional effort applied that is not done in prior projects. This effort includes styling and configuring the page to allow scrolling for smaller screens.

Tsilal is designed to be distinct from all other projects in this course. This can be conferment as none of the prior projects are aimed at building a hotel webpage or any reservation system. And as a final assessment of the course, lots of the skills acquired are implemented in the project. An email system is integrated in the project, and it is implemented to send a confirmation of a booking to a user. This email system is not a priori to Project 4 – network. As the email system is done through a built-in Django’s mail system. This feature is added to the project to reach a certain level of complexity and to fulfil typical requirements of a hotel system. 


## How to run
The web application can be run through any python interpreter tool. It can be run by surfing to the project and executing “python manage.py runserver”.


## Additional info
Note that the dimensions, that best suit the mobile site pages, is 400x865.
In addition, because an email is sent out after a succesful booking though mailstrap.io and as Django requires using the use of "EMAIL_HOST_USER" and "EMAIL_HOST_PASSWORD" in "/settings.py" I have used them while developing the webpage. But, as the repository I initially pushed is public I have commented them out. So, prior to running the project, an account from "mailtrap.io" is required. Check out this link (https://mailtrap.io/blog/django-send-email/) for more info.
