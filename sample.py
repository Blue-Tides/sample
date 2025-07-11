### importing libraries ###
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp

### data extraction ###

#data from US Census Bureau

#csv extracting
def read_csv(filename: str):
    file = open(filename)
    filearr = []
    for line in file:
        linearr = line.split(",")
        if(linearr[-1] == "\n" or linearr[-1]==""):
            linearr=linearr[:-1]
        filearr.append(list(map(float, linearr)))
    file.close()
    return filearr

#file reading
data=read_csv("2020.csv")
data.extend(read_csv("2024.csv"))

### convert into dataframe for easier processing ###

#adding extra attributes
age_groups=["all","18-24","24-44","45-64","65-74","75+"]
for i in range(len(data)):
    #add attribute gender
    if(i%18<6): 
        data[i].append("all")
    elif (i%18<12):
        data[i].append("male")
    else:
        data[i].append("female")
    
    #add attribute age group
    data[i].append(age_groups[i%6])

    #add margin of error attribute (whether row represents number or margin of error)
    data[i].append(i%36>=18)
    
    #add year attribute
    data[i].append("2020" if i<36 else "2024")

df=pd.DataFrame(data,columns=["total_population","citizen_population","registered_number","registered_percentage","no_registered_number","no_registered_percentage","no_response_number","no_response_percentage","voted_number","voted_percentage","no_voting_number","no_voting_percentage","no_response_voting_number","no_response_voting_percentage","total_registered_percentage","total_voted_percentage","sex","age_group","margin_of_error","year"])

### graph generating ###

#proportion of citizens grouped by gender, subdivided by age group
def voting_citizen(year,dataframe,ax):
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])
    df=dataframe.loc[(dataframe["year"]==str(year)) & ~dataframe["margin_of_error"]]
    total_pop=df.loc[(df["age_group"]=="all") & (df["sex"]=="all"),"citizen_population"].iloc[0]
    df=df.loc[dataframe["age_group"] != "all"]
    df_f=df.loc[df["sex"]=="female"]

    df_f_cp=df_f["citizen_population"]
    widths_f=(df_f_cp/total_pop)
    x_f=[0]
    for i in range(len(widths_f)):
        x_f.append(widths_f.iloc[i]+x_f[-1])

    ax.bar_label(ax.bar(x_f[:-1],df_f["voted_number"]/df_f_cp,width=widths_f,align="edge",linewidth=1,edgecolor="black",color="pink",label="Female"),labels=age_groups[1:],label_type='center',rotation=90)
    df_m=df.loc[df["sex"]=="male"]
    df_m_cp=df_m["citizen_population"]
    widths_m=(df_m_cp/total_pop)
    x_m=x_f[-1:]
    for i in range(len(widths_f)-1):
        x_m.append(widths_m.iloc[i]+x_m[-1])

    ax.bar_label(ax.bar(x_m,df_m["voted_number"]/df_m_cp,width=widths_m,align="edge",linewidth=1,edgecolor="black",
    color="cyan",label="Male"),labels=age_groups[1:],label_type='center',rotation=90)
    ax.get_xaxis().set_visible(False)


#grouped by age, subdivided by gender
def voting_citizen_1(year,dataframe,ax):
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])
    df=dataframe.loc[(dataframe["year"]==str(year)) & ~dataframe["margin_of_error"]]
    total_pop=df.loc[(df["age_group"]=="all") & (df["sex"]=="all"),"citizen_population"].iloc[0]
    df=df.loc[dataframe["age_group"]!="all"]
    df_f=df.loc[df["sex"]=="female"]

    df_f_cp=df_f["citizen_population"]
    widths_f=(df_f_cp/total_pop)
    df_m=df.loc[df["sex"]=="male"]
    df_m_cp=df_m["citizen_population"]
    widths_m=(df_m_cp/total_pop)
    x=[0]
    for i in range(len(widths_f)):
        x.append(widths_f.iloc[i]+x[-1])
        x.append(widths_m.iloc[i]+x[-1])

    ax.bar_label(ax.bar(x[0:-2:2],df_f["voted_number"]/df_f_cp,width=widths_f,align="edge",linewidth=1,edgecolor="black",color="pink",label="Female"),labels=age_groups[1:],label_type='center',rotation=90)
    ax.bar_label(ax.bar(x[1::2],df_m["voted_number"]/df_m_cp,width=widths_m,align="edge",linewidth=1,edgecolor="black",
    color="cyan",label="Male"),labels=age_groups[1:],label_type='center',rotation=90)
    ax.get_xaxis().set_visible(False)
    
    
### sample statistical calculation ###

### render ###
fig, axes = plt.subplots(2,2)
voting_citizen(2020,df,axes[0][0])
voting_citizen(2024,df,axes[1][0])
voting_citizen_1(2020,df,axes[0][1])
voting_citizen_1(2024,df,axes[1][1])

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
fig.legend(by_label.values(), by_label.keys())

fig.suptitle("Voter Turnout by Age Group and Gender")
fig.supylabel("Proportion of Citizens who Voted")
axes[0][0].set_ylabel("2020")
axes[1][0].set_ylabel("2024")

fig.tight_layout()
plt.show()


