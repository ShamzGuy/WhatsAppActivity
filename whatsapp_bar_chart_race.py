import pandas as pd
from collections import defaultdict
import bar_chart_race as bcr # version used in this code is bar-chart-race 0.1.0

def create_race_vid(fname, vidname):

    with open(fname, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    date = []
    user = []
    num_words = []
    for line in lines:
        try:
            if "Media omitted" in line:
                continue
            d = line.split(",")[0]
            d = pd.to_datetime(d, infer_datetime_format=True, format="%Y%m%d")
            u = line.split(" - ")[1].split(":")[0].strip()
            t = line.split(u + ":")[1]
            n = len(t.split())
        except:
            continue
        date.append(d)
        user.append(u)
        num_words.append(n)

    z = {"Date": date, "User": user, "Count": num_words}
    df = pd.DataFrame(z, columns=["Date", "User", "Count"], index=None)

    date_count_df = df.groupby(["Date", "User"])["Count"].sum().reset_index()

    cdict = defaultdict(int)

    for index, row in date_count_df.iterrows():
        user = row["User"]
        cdict[user] += row["Count"]
        date_count_df.loc[index, "Count"] = cdict[user]

    df_values, df_ranks = bcr.prepare_long_data(
        date_count_df, index="Date", columns="User", values="Count", steps_per_period=5
    )
    df_values.head(16)

    bcr.bar_chart_race(df=df_values, filename=vidname, period_length=75)


if __name__ == "__main__":

    fname = input("Please enter text file name: ")
    vidname = input("Please enter desired video name: ")
    create_race_vid(fname, vidname)
