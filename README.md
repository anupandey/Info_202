# Info_202

Our project, Chalk Street aggregates a set of courses available for topics such as computer science, machine learning, natural language processing and related topics and presents a method for our users to retrieve these courses based on metrics that we believe would help our users to  search and find courses that better match with their need and capability and thus support them in making an appropriate course selection.

Description of our Resource:
For our ‘course catalogue’ organising system, a resource is an individual, independent online course. We treat our resource as unitary. The level of  granularity of at which we are describing our resource is at the level of course i.e each course is identified as a separate course. Courses that have the same title, that are offered by the same institution and instructor were treated as identical for the purpose of our classification. The definition for identical courses was defined even before the classification since we assumed there is a possibility of finding a course across multiple platforms such as Coursera, Udacity, EdX, Udemy, NPTEL etc. The courses were offered in different languages and were offered by different platforms and institutions ranging from University of California, Berkeley to University of Denmark (DTU).

Our Method:				
Identify categories - For our project, we have identified categories that can help a course-taker/student achieve a goal of selecting the best course suited to his/her needs (type, institution, ratings, self-paced etc. ) in a given time (number of weeks) for a given time frame (offered now, offered later). 

The following attributes were selected and extracted for organizing the courses in Chalk street:
1. Title
2. Subject
3. Summary
4. Description
5. Provider
6. Instructors
7. Institute
8. Reviews
9. Review Count
10. Rating
11. Session start date
12. Course Pace
13. Language
14. Duration 
15.Commitment (hrs/week)
16. Certification
17. Price
18. Course URL’s

Crawling Data - Since our system is able to implement the functionality of multi- site search, our first task was to be able to crawl course data from the major course websites. Before crawling, we identified a set of categories (mentioned below) that we felt can belt help the user in his/her search of selecting the perfect course. The data available (choice of displayed categories) from different websites such as coursera, Udacity, NPTEL was displayed in a different  format (some categories were absent or not very detailed if a course was offered by a specific provider) and thus served a limiting factor for the choice of classification we developed. Beautiful soup library was used by us to crawl the data.

Data Parsing - we wrote a python script to parse and match the keywords in each crawled files to extract information such as description, Title, duration, institution, instructors, hours per week, course level etc and formed a list of courses. Initially we could crawl on 200+ courses but we came back to step 1 and 2 to pool more courses, once we realized our data set was small for providing us relevant results when concepts/principles of cosine-similarity was applied to find courses similar to a particular 	course(course that best meets the filters selected by our user). In the end we could increase our number of courses from 200+ to 2200+. The greater number of course helped us to allow user to filter their search and yield a refined output of courses.

Develop a classification system - Our classification system of assigning resources into different categories. As per our rationale behind classification, the course categorization system developed by us consisted of different types of categories such as classical, cultural, individual etc. 

Develop a resource (course) retrieval system by utilizing Index and Search Implementation, cosine similarity - After crawling and extracting the features from the crawled data, we will build up an index among the files 



