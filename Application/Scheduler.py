"""
11/18/18
Array of 24 empty elements (if scheduling by 30 min session 48 elements)
Monday=[12 am, 1 am, 2 am, 3 am, 4 am, 5 am, 6 am, 7 am, 8 am, 9 am, 10 am, 11 am, 12 pm, 1 pm, 2 pm, 3 pm, 4 pm, 5 pm, 6 pm, 7 pm, 8 pm, 9 pm, 10 pm, 11 pm] element resembles time slot
Beginning prompt to enter school schedule
eg) Enter Class Name : Science
			time : 11 am - 1pm
			days : M,W

Monday=[12 am, 1 am, 2 am, 3 am, 4 am, 5 am, 6 am, 7 am, 8 am, 9 am, 10 am, Science, Science, Science, 2 pm, 3 pm, 4 pm, 5 pm, 6 pm, 7 pm, 8 pm, 9 pm, 10 pm, 11 pm]
Wednesday=[12 am, 1 am, 2 am, 3 am, 4 am, 5 am, 6 am, 7 am, 8 am, 9 am, 10 am, Science, Science, Science, 2 pm, 3 pm, 4 pm, 5 pm, 6 pm, 7 pm, 8 pm, 9 pm, 10 pm, 11 pm]

After filling schedule

Enter Sleep Schedule
			time: 12am - 9am

Monday=[Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, 10 am, Science, Science, Science, 2 pm, 3 pm, 4 pm, 5 pm, 6 pm, 7 pm, 8 pm, 9 pm, 10 pm, 11 pm]

etc...

Monday=[Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Bekfast, Science, Science, Science, Lunch, open, open, open, open, open, Dinnah, open, open, open]
Tuesday=[Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Bekfast, Science, Science, Science, Lunch, Math, Math, open, open, open, Dinnah, open, open, open]

Task Scheduler
Enter name of task: <Task_Name>
Enter Est time for completion: # of hours
Prefernce time of day: Options: Morning(4am-11am), Mid day(12pm-5pm), Night(6pm-3am)
Due Date: Day of the week due - expand to picking day of month

eg)
Enter name of task: Science Project
Enter Est time for completion: 5
Prefernce time of day: Options: Night
Due Date: Day of the week due - Wednesday

Desired -
Monday=[Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Bekfast, Science, Science, Science, Lunch, open, open, open, open, open, Dinnah, open, open, open]
Tuesday=[Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Sleep, Bekfast, Science, Science, Science, Lunch, Math, Math, open, open, open, Dinnah, open, open, open]

1. Split est time for completion into max number of days before deadline
2. keep counter for actually available days eg) if selected for night and the time slots are occupied
eg) due thursday, inputted sunday, 3 hrs to complete
monday add in 1 hr success - hrs to fill is 2
tuesday unsucessful - hrs to fill is 2
wednesday add in 3 hr success - hrs to fill is 0


"""

