/*Import CSV file into SAS dataset */
DATA forestfires;
    INFILE "/home/u63840069/Project/forestfires.csv" DELIMITER=',' DSD FIRSTOBS=2;
    INPUT X Y Month $ Day $ FFMC DMC DC ISI Temp RH Wind Rain Area;
RUN;


/* User-defined formats for month and day for printing data*/
proc format;
    value $month_fmt
        'jan' = 'January'
        'feb' = 'February'
        'mar' = 'March'
        'apr' = 'April'
        'may' = 'May'
        'jun' = 'June'
        'jul' = 'July'
        'aug' = 'August'
        'sep' = 'September'
        'oct' = 'October'
        'nov' = 'November'
        'dec' = 'December';
    value $day_fmt
        'mon' = 'Monday'
        'tue' = 'Tuesday'
        'wed' = 'Wednesday'
        'thu' = 'Thursday'
        'fri' = 'Friday'
        'sat' = 'Saturday'
        'sun' = 'Sunday';
run;


title "Data collected about the forest fires";
proc print data=forestfires;
    format month $month_fmt. day $day_fmt.;
run;


/* Calculate average temperature and total area burned per month */
proc sql;
    create table monthly_summary as
    select Month, 
           mean(Temp) as Avg_Temp, 
           sum(Area) as Total_Area
    from forestfires
    group by Month;
quit;

/* Combining data sets */
proc sort data=forestfires; 
    by Month;
run;

data combined_fires;
    merge forestfires(in=a) monthly_summary(in=b);
    by month;
    if a and b;
run;


/* Flagging the high risk areas*/
DATA forestfires;
    INFILE "/home/u63840069/Project/forestfires.csv" DELIMITER=',' DSD FIRSTOBS=2;
    INPUT X Y $ Month $ Day $ FFMC DMC DC ISI Temp RH Wind Rain Area;
    
    if not missing(Temp) and not missing(Wind) and not missing(RH) then do;
        if Temp > 27 and Wind > 5 and RH < 35 then High_Risk = 1;
        else High_Risk = 0;
    end;
    else High_Risk = .;
RUN;


proc freq data=forestfires;
    tables High_Risk / nocum;
    title "Frequency of High-Risk Fire Conditions";
run;

/* Categorizing the temperature*/
DATA forestfires;
    INFILE "/home/u63840069/Project/forestfires.csv" DELIMITER=',' DSD FIRSTOBS=2;
    INPUT X Y $ Month $ Day $ FFMC DMC DC ISI Temp RH Wind Rain Area;

    LENGTH Temp_Category $ 6;
    if Temp < 15 then Temp_Category = 'Low';
    else if 15 <= Temp < 25 then Temp_Category = 'Medium';
    else if Temp >= 25 then Temp_Category = 'High';
RUN;

proc freq data=forestfires;
    tables Temp_Category / nocum;
    title "Distribution of Temperature Categories";
run;


/* Univariate analysis on temperature and area burned */
proc univariate data=forestfires;
    var Temp;
    histogram Temp;
    title "Univariate Analysis of Temperature";
run;


/* Linear regression analysis */
proc reg data=forestfires;
    model Area = Temp RH Wind Rain;
    title "Linear Regression Analysis of Area Burned";
run;


/* Define seasons based on month */
DATA forestfires;
    INFILE "/home/u63840069/Project/forestfires.csv" DELIMITER=',' DSD FIRSTOBS=2;
    INPUT X Y $ Month $ Day $ FFMC DMC DC ISI Temp RH Wind Rain Area;

    if Month in ('jan', 'feb', 'mar') then Season = 'Winter';
    else if Month in ('apr', 'may', 'jun') then Season = 'Spring';
    else if Month in ('jul', 'aug', 'sep') then Season = 'Summer';
    else if Month in ('oct', 'nov', 'dec') then Season = 'Fall';
RUN;


proc gchart data=forestfires;
    pie Season / percent=inside;
    title "Distribution of Records by Season";
run;
quit;


