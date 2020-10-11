#!/usr/local/bin/python3

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotMostChanged():
    df = pd.read_csv("./mostChanged.csv")
    df = df[df['n-revs']>15]
    df = df.sort_values(['n-revs'], ascending=[False])
    names = df['entity'].values
    x = np.arange(len(names))
    w = 0.5
    plt.figure(figsize=[15.0, 10.0])
    plt.bar(x, df['n-revs'].values, width=w, label='n-revs')
    plt.bar(x, df['n-authors'].values, width=w, label='n-authors')
    plt.xticks(x, names, rotation='vertical')
    plt.yticks(np.arange(0, 175, step=10)) 
    plt.plot(x, df['n-revs'].values, lw=2)
    plt.plot(x, np.full(len(names), 20), lw=2, color='red', label="20 revs")
    plt.ylim([0,175])
    plt.xlabel('X label')
    plt.legend()
    plt.title('Most often changed files in the last year (since 30.09.2020)')
    plt.savefig("mostChanged.svg", bbox_inches="tight", format="svg")
    plt.show()

def plotAbsChurn():
    df = pd.read_csv("./abs-churn.csv")
    date = df['date'].values
    x = np.arange(len(date))
    fig, ax = plt.subplots(figsize=(25.0, 10.0))
    
    ax.set_xticks(np.arange(len(date)))
    ax.set_yticks(np.arange(0, 5600, step=100)) 
    ax.set_xticklabels(date)
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")

    temp = ax.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::7]))
    for label in temp:
        label.set_visible(False)

    plt.plot(x, df['added'].values, lw=1, label="added", color="green")
    plt.plot(x, df['deleted'].values, lw=1, color='red', label="deleted", linestyle='dashed')
    plt.plot(x, [x*100 for x in df['commits'].values], lw=1, color='blue', label="commits*100", linestyle='dotted')
    plt.legend()
    plt.title('Added vs deleted lines until today')
    plt.savefig("abs-churn.svg", bbox_inches="tight", format="svg")
    plt.show()


def plotCommits():
    df = pd.read_csv("./abs-churn.csv")
    date = df['date'].values
    x = np.arange(len(date))
    fig, ax = plt.subplots(figsize=(25.0, 10.0))
    
    ax.set_xticks(np.arange(len(date)))
    ax.set_yticks(np.arange(0, 50, step=5)) 
    ax.set_xticklabels(date)
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")

    temp = ax.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::7]))
    for label in temp:
        label.set_visible(False)

    plt.plot(x, df['commits'].values, lw=1, label="added", color="blue")
    plt.legend()
    plt.title('Commits until today')
    plt.savefig("commits.svg", bbox_inches="tight", format="svg")
    plt.show()

def plotAuthorChurn():
    df = pd.read_csv("./authors_churn_unknown.csv")
    author = df['author'].values
    x = np.arange(len(author))
    fig, ax = plt.subplots(figsize=(15.0, 10.0))
    
    
    ax.set_xticks(np.arange(len(author)))
    ax.set_yticks(np.arange(0, 40000, step=1000)) 
    ax.set_xticklabels(author)
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")

    w = 0.3
    plt.figure(figsize=[15.0, 10.0])
    ax.bar(x-w, df['added'].values, width=w, label='added', color="green")
    ax.bar(x, df['deleted'].values, width=w, label='deleted', color="red")
    ax.bar(x+w, [x*10 for x in df['commits'].values], width=w, label='commits*10',color="blue")
    ax.legend()
    ax.set_title('Added vs deleted lines until today')
    fig.savefig("author-churn.svg", bbox_inches="tight", format="svg")
    plt.show()


def createSummaryCsv():
    os.system("java -jar code-maat-1.1-SNAPSHOT-standalone.jar -l logfile.log -c git2 -a summary> summary.csv")

def createMostChangedCsv():
    os.system("java -jar code-maat-1.1-SNAPSHOT-standalone.jar -l logfile.log -c git2 > mostChanged.csv")

def createAbsChurnCsv():
    os.system("java -jar code-maat-1.1-SNAPSHOT-standalone.jar -l logfile.log -c git2 -a abs-churn > abs-churn.csv")

def createCouplingCsv():
    os.system("java -jar code-maat-1.1-SNAPSHOT-standalone.jar -l logfile.log -c git2 -a coupling > coupling.csv")

def createAuthorChurnCsv():
    os.system("java -jar code-maat-1.1-SNAPSHOT-standalone.jar -l logfile.log -c git2 -a author-churn > author-churn.csv")

def createCommitsCsv():
    os.system("java -jar code-maat-1.1-SNAPSHOT-standalone.jar -l logfile.log -c git2 -a abs-churn > abs-churn.csv")

def createlogfile(date):
    os.system("git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames --after={} > logfile.log".format(date))

createlogfile("2020-09-30")
createSummaryCsv()
createMostChangedCsv()
createAbsChurnCsv()
createCouplingCsv()
createAuthorChurnCsv()
createCommitsCsv()
plotMostChanged()
plotAbsChurn()
plotAuthorChurn()
plotCommits()
