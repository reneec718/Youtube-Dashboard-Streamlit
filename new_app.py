import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import time
import plotly.express as px

if "gaming_button" not in st.session_state:
    st.session_state.gaming_button = False
if "movies_button" not in st.session_state:
    st.session_state.movies_button = False
if "music_button" not in st.session_state:
    st.session_state.music_button = False
if 'load_app' not in st.session_state:
    st.session_state.load_app = False

def reset_all_tabs():
    st.session_state.gaming_button = False
    st.session_state.movies_button = False
    st.session_state.music_button = False

def activate_tab(tab_key):
    reset_all_tabs()
    st.session_state[tab_key] = True

# set page
st.set_page_config(page_title="YouTube Dashboard", page_icon="🎬", layout="wide")
# set tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📑 Introduction", "🎮 Gaming", "📽️ Movies", "🎵 Music", "🔏 Improvement"])

# df_gaming = pd.read_csv("pages/data/gaming.csv")
df_gaming = pd.read_csv("gaming.csv")
df_movie = pd.read_csv("movies.csv")
df_music = pd.read_csv("music.csv")

######################################################################### INTRODUCTION #######################################################################
with tab1:
    # Application introduction
    st.title("🎬 YouTube Data Analysis Dashboard")
    st.write("""
    Welcome to the **YouTube Data Analysis App**!  
    This application provides insights into YouTube videos across different categories, helping users understand trends, engagement metrics, and popular content.
    """)

    # Dataset overview
    st.subheader("Dataset Column Explaination")
    st.write("""
    The dataset used in this analysis comes from YouTube and contains key attributes such as:
    - **title:** title of the video
    - **description:** description of the vide
    - **publishedDate:** the date when the video is published 
    - **channelName:** the channel that published the video
    - **views:** the number of views
    - **duration:** the length of the video (seconds)
    - **isShort:** if the video is categorized as shorts
    """)
    st.markdown("---")
    st.subheader("Dataset Statistics")   
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Gaming")
        # Dataset statistics
        st.write(df_gaming.describe())
        # Dataset size
        st.write(f"🔹 Total Videos: {df_gaming.shape[0]}")
        st.write(f"🔹 Total Columns: {df_gaming.shape[1]}")
    with col2:
        st.write("Movies")
        # Dataset statistics
        st.write(df_movie.describe())
        # Dataset size
        st.write(f"🔹 Total Videos: {df_movie.shape[0]}")
        st.write(f"🔹 Total Columns: {df_movie.shape[1]}")
    with col3:
        st.write("Music")
        # Dataset statistics
        st.write(df_music.describe())
        # Dataset size
        st.write(f"🔹 Total Videos: {df_music.shape[0]}")
        st.write(f"🔹 Total Columns: {df_music.shape[1]}")
    st.markdown("---")
    # Preview data
    st.subheader("Dataset Preview") 
    st.write("Gaming Dataset")
    st.dataframe(df_gaming.head())

    st.write("Movie Dataset")
    st.dataframe(df_movie.head())

    st.write("Music Dataset")
    st.dataframe(df_music.head())


############################################################################ GAMING ##########################################################################
with tab2:
    # publishedDate to date
    df_gaming["publishedDate"] = pd.to_datetime(df_gaming["publishedDate"]).dt.date

    st.title("🎮 Gaming")

    # card
    col1, col2, col3 = st.columns(3)
    with col1:
        ttl_video = df_gaming["title"].count()
        st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}")
    with col2:
        ttl_duration = df_gaming["duration"].sum()
        st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}")
    with col3: 
        ttl_view = df_gaming["views"].sum()
        st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}")


    # line: avg view vs. date
    df_gaming_1 = df_gaming.groupby("publishedDate")["views"].mean().reset_index()
    overall_avg = df_gaming["views"].mean()
    g1 = px.line(df_gaming_1,
                x="publishedDate",
                y="views", 
                title="Monthly Average View",
                color_discrete_sequence=px.colors.qualitative.Pastel)
    # avg line
    g1.add_hline(y=overall_avg, 
                line_color="#ec5353",
                line_dash="dash",
                annotation_text=f"Overall Mean: {overall_avg:.2f}",
                annotation_position="top right")
    st.plotly_chart(g1, use_container_width=True)


    # subplots
    col1, col2 = st.columns(2)

    # small plot left: 時長
    with col1:
            st.subheader("📊 Top Views Channel")
            # Top views - Channel
            df_gaming_2 = df_gaming.groupby("channelName")["views"].sum().reset_index()
            df_gaming_2 = df_gaming_2.sort_values("views", ascending=False)

            max_channels_views_gaming = min(len(df_gaming_2), 20)
            num_channels_views_gaming = st.slider("📏 Number of Gaming Channel_views", min_value = 1, max_value = max_channels_views_gaming, value = 5)
            top_channelview = df_gaming_2.head(num_channels_views_gaming)

            g2 = px.bar(top_channelview, x = "views", y = "channelName", orientation = "h",
                  labels = {"views": "Total Views", "channelName": "Channel Name"},
                  title = f"🔥 Channel Video Count Top {num_channels_views_gaming}", color="channelName",
                  color_discrete_sequence = px.colors.qualitative.Pastel)
            g2.update_layout(showlegend=False)
            st.plotly_chart(g2, use_container_width=True)

    with col2:
        st.subheader("📊 Top Video Published Channel")
        df_gaming_3 = df_gaming["channelName"].value_counts().reset_index()
        df_gaming_3 = df_gaming_3.sort_values("count", ascending=False)
        df_gaming_3 = df_gaming_3.rename(columns={"count":"Num of Video"})

        max_channels_count_gaming = min(len(df_gaming_3), 20)
        num_channels_count_gaming = st.slider("📏 Number of Gaming Channel_count", min_value = 1, max_value = max_channels_count_gaming, value = 5)
        top_channels = df_gaming_3.head(num_channels_count_gaming)

        g3 = px.bar(top_channels, x = "Num of Video", y = "channelName", orientation = "h",
                labels = {"Num of Video": "Count", "channelName": "Channel Name"},
                title = f"🔥 Channel Video Count Top {num_channels_count_gaming}", color="channelName",
                color_discrete_sequence = px.colors.qualitative.Pastel)
        g3.update_layout(showlegend=False)
        st.plotly_chart(g3, use_container_width = True)

    ####################################################################################
    # button 
    # def click_button():
        # st.session_state.gaming_button = True
    # button for detailed nalysis
    # st.button('Detailed Analysis', on_click=click_button)
    # 🚀 Gaming Tab 按鈕
    if st.button("Detailed Analysis - Gaming", key = "gaming_analysis"):
        activate_tab("gaming_button")
        st.session_state.gaming_button = True
        st.session_state.movies_button = False  # 確保 Movies 相關內容關閉
        st.session_state.music_button = False

    if st.session_state.gaming_button:
        st.subheader("📈 Channel Analysis")
        # select date
        start_date = df_gaming["publishedDate"].min()
        end_date = df_gaming["publishedDate"].max()
        options_date = st.sidebar.date_input("Publish Date",
                            (start_date, end_date),
                            start_date, end_date,
                            key = "gaming_date")
        # select channel
        df_gaming_uni_channel = df_gaming.drop_duplicates("channelName")
        channel_option = df_gaming_uni_channel.sort_values("channelName", ascending=True)["channelName"]
        options_channel = st.sidebar.selectbox("📌 Gaming Channel", channel_option)

        # Display a message
        # st.write('Gaming Trending Video DataFrame')
        # Generate a dataframe and display it in the app
        # st.dataframe(df_gaming.head(10))

        # views & duration
        with st.sidebar.expander("More Filtering", expanded=False):
            min_views = int(df_gaming["views"].min())
            max_views = int(df_gaming["views"].max())
            min_views_formatted = f"{min_views:,}"
            max_views_formatted = f"{max_views:,}"
            min_views = st.number_input("Min Views", min_value=int(min_views), value=int(min_views))
            max_views = st.number_input("Max Views", max_value=int(max_views), value=int(max_views))

            min_duration = df_gaming["duration"].min()
            max_duration = df_gaming["duration"].max()
            min_duration = st.number_input("Min Duration (seconds)", min_value=int(min_duration), value=int(min_duration))
            max_duration = st.number_input("Max Duration (seconds)", max_value=int(max_duration), value=int(max_duration))

        # card
        col1, col2, col3 = st.columns(3)
        with col1:
            mask = df_gaming["publishedDate"].between(options_date[0], options_date[1]) & df_gaming["channelName"].isin([options_channel])      
            df_filtered_1 = df_gaming[mask]
            ttl_video = df_filtered_1["title"].count()
            st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}")
        with col2:
            ttl_duration = df_filtered_1["duration"].sum()
            st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}")
        with col3: 
            ttl_view = df_filtered_1["views"].sum()
            st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}")

        # plot1: top view per day
        if options_date and options_channel:
            mask = df_gaming["publishedDate"].between(options_date[0], options_date[1]) &\
                    df_gaming["channelName"].isin([options_channel])
            df_filtered_1 = df_gaming[mask]

            df_gaming_1 = df_filtered_1.groupby(["publishedDate", "channelName"])["views"].mean().reset_index()
            g1 = px.line(df_gaming_1,
                        x= "publishedDate",
                        y= "views",
                        title = "Top View Per Day",
                        markers = True,
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            g1.add_hline(y=overall_avg, 
                         line_color="#ec5353",
                         line_dash="dash",
                         annotation_text=f"Overall Mean: {overall_avg:.2f}",
                         annotation_position="top right")
            st.plotly_chart(g1, use_container_width=True)
                
        if options_date and not options_channel:
            mask = df_gaming["publishedDate"].between(options_date[0], options_date[1])
            df_filtered_1 = df_gaming[mask]

            df_gaming_1 = df_filtered_1.groupby(["publishedDate"])["views"].mean().reset_index()
            g1 = px.line(df_gaming_1,
                            x="publishedDate",
                            y="views",
                            title = "Top View Per Day",
                            markers = True,
                            color_discrete_sequence=px.colors.qualitative.Pastel)
            g1.add_hline(y=overall_avg, 
                            line_color="#ec5353",
                            line_dash="dash",
                            annotation_text=f"Overall Mean: {overall_avg:.2f}",
                            annotation_position="top right")
            st.plotly_chart(g1, use_container_width=True)

    # Two small graphs
    if st.session_state.gaming_button:
        col1, col2 = st.columns([3, 2])
        # top 10 video per channel
        with col1:
            mask = df_gaming["channelName"].isin([options_channel]) &\
                    df_gaming['duration'].between(min_duration, max_duration) &\
                    df_gaming['views'].between(min_views, max_views)
            df_filtered_2 = df_gaming[mask]
            top_videos = df_filtered_2.sort_values("views", ascending=False).head(10)
            g2 = px.bar(top_videos, x="views", y="title",
                        title="🔥 Top 10 Videos by View",
                        color="title",
                        color_discrete_sequence = px.colors.qualitative.Pastel)
            g2.update_layout(showlegend=False)
            st.plotly_chart(g2, use_container_width=True)
        
        with col2:
            mask = df_gaming["channelName"].isin([options_channel]) &\
                    df_gaming['duration'].between(min_duration, max_duration) &\
                    df_gaming['views'].between(min_views, max_views)
            df_filtered_3 = df_gaming[mask]
            g3 = px.scatter(df_filtered_3, x="duration", y="views",
                            title="⏳ Duration vs. Views",
                            size="views",
                            color_discrete_sequence = px.colors.qualitative.Pastel)
            g3.update_layout(showlegend=False)
            st.plotly_chart(g3, use_container_width=True)

    # table
    if st.session_state.gaming_button:
        mask = df_gaming["channelName"].isin([options_channel]) &\
                df_gaming['duration'].between(min_duration, max_duration) &\
                df_gaming['views'].between(min_views, max_views)
        df_filtered_4 = df_gaming[mask].drop(columns=["channelName"])

        st.write('📊 Gaming Video Dataframe')
        st.dataframe(df_filtered_4)


###################################################################### MOVIE #################################################################################
    with tab3:
        df_movie["publishedDate"] = pd.to_datetime(df_movie["publishedDate"]).dt.date

        st.title("📽️ Movies")
        # card
        col1, col2, col3 = st.columns(3)
        with col1:
            ttl_video = df_movie["title"].count()
            st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}")
        with col2:
            ttl_duration = df_movie["duration"].sum()
            st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}")
        with col3: 
            ttl_view = df_movie["views"].sum()
            st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}")

        # line: avg view vs. date
        df_date = df_movie.groupby("publishedDate")["views"].mean().reset_index(name = "max_views")
        overall_avg = df_movie["views"].mean()
        fig = px.line(df_date, x = 'publishedDate', y= 'max_views', title= 'Daily Average Views', color_discrete_sequence=px.colors.qualitative.Pastel)
        # avg line
        fig.add_hline(y = overall_avg, line_color="#ec5353", line_dash="dash", annotation_text=f"Overall Mean: {overall_avg:.2f}", annotation_position="top right")
        st.plotly_chart(fig, use_container_width=True)

        # subplots
        col1, col2 = st.columns(2)
        # small plot left: 時長
        with col1:
            # Top 10 views - Channel
            df_channelview = df_movie.groupby("channelName")["views"].sum().reset_index(name = "sum_views")
            df_channelview = df_channelview.sort_values('sum_views', ascending = False)
            # top10_channels = df_channelview.head(10)  # top 10

            st.subheader("📊 Top Views Channel")
            max_channels_views = min(len(df_channelview), 20)
            num_channels_views = st.slider("📏 Number of Movie Channel_views", min_value = 1, max_value = max_channels_views, value = 5)
            top_channelview = df_channelview.head(num_channels_views)

            fig1 = px.bar(top_channelview, x = "sum_views", y = "channelName", orientation = "h",
                  labels = {"sum_views": "Total Views", "channelName": "Channel Name"},
                  title = f"🔥 Channel Video Count Top {num_channels_views}", color="channelName",
                  color_discrete_sequence = px.colors.qualitative.Pastel)
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            channel_video_counts = df_movie['channelName'].value_counts().reset_index(name = 'video_count')
            
            st.subheader("📊 Top Video Published Channel")
            max_channels_count = min(len(channel_video_counts), 20)
            num_channels_count = st.slider("📏 Number of Movie Channel_count", min_value = 1, max_value = max_channels_count, value = 5)
            top_channels = channel_video_counts.head(num_channels_count)

            fig2 = px.bar(top_channels, x = "video_count", y = "channelName", orientation = "h",
                  labels = {"video_count": "Count", "channelName": "Channel Name"},
                  title = f"🔥 Channel Video Count Top {num_channels_count}", color="channelName",
                  color_discrete_sequence = px.colors.qualitative.Pastel)
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        ####################################################################################
        # button 
        # def click_button():
            #st.session_state.movies_button = True
        # button for detailed nalysis
        # st.button('Detailed Analysis', on_click=click_button)

        # 🚀 Movies Tab 按鈕
        if st.button("Detailed Analysis - Movies", key = "movies_analysis"):
            activate_tab("movies_button")
            st.session_state.movies_button = True
            st.session_state.gaming_button = False  # 確保 Gaming 相關內容關閉
            st.session_state.music_button = False

        if st.session_state.movies_button:
            st.subheader("📈 Channel Analysis")
             # select date
            start_date = df_movie["publishedDate"].min()
            end_date = df_movie["publishedDate"].max()
            options_date = st.sidebar.date_input("Publish Date",
                                (start_date, end_date),
                                start_date, end_date,
                                key = 'movie_date')
            # select channel
            channel_list = sorted(df_movie['channelName'].unique()) 
            selected_channels = st.sidebar.selectbox("📌 Movie Channel", channel_list)

            # Display a message
            # st.write('Movies Trending Video DataFrame')
            # Generate a dataframe and display it in the app
            # st.dataframe(df_movie.head(10))

            # views & duration
            with st.sidebar.expander("More Filtering", expanded=False):
                min_views = df_movie["views"].min()
                max_views = df_movie["views"].max()
                min_views = st.number_input("Min Views", min_value=int(min_views), value=int(min_views))
                max_views = st.number_input("Max Views", max_value=int(max_views), value=int(max_views))

                min_duration = df_movie["duration"].min()
                max_duration = df_movie["duration"].max()
                min_duration = st.number_input("Min Duration (seconds)", min_value=int(min_duration), value=int(min_duration))
                max_duration = st.number_input("Max Duration (seconds)", max_value=int(max_duration), value=int(max_duration))

            # card
            col1, col2, col3 = st.columns(3)
            with col1:
                mask = df_movie["publishedDate"].between(options_date[0], options_date[1]) & df_movie["channelName"].isin([selected_channels])      
                df_filtered_1 = df_movie[mask]
                ttl_video = df_filtered_1["title"].count()
                st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}")
            with col2:
                ttl_duration = df_filtered_1["duration"].sum()
                st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}")
            with col3: 
                ttl_view = df_filtered_1["views"].sum()
                st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}")

            # plot1: top view per day
            if options_date and selected_channels:
                mask = df_movie["publishedDate"].between(options_date[0], options_date[1]) &\
                        df_movie["channelName"].isin([selected_channels])
                df_filtered_1 = df_movie[mask]

                df_movie_1 = df_filtered_1.groupby(["publishedDate", "channelName"])["views"].mean().reset_index()
                fig3 = px.line(df_movie_1,
                            x = "publishedDate",
                            y = "views",
                            title = "Top View Per Day",
                            markers = True,
                            color_discrete_sequence=px.colors.qualitative.Pastel)
                fig3.add_hline(y = overall_avg, 
                            line_color = "#ec5353",
                            line_dash = "dash",
                            annotation_text = f"Overall Mean: {overall_avg:.2f}",
                            annotation_position = "top right")
                st.plotly_chart(fig3, use_container_width=True)
                    
            if options_date and not selected_channels:
                mask = df_movie["publishedDate"].between(options_date[0], options_date[1])
                df_filtered_1 = df_movie[mask]

                df_movie_1 = df_filtered_1.groupby(["publishedDate"])["views"].mean().reset_index()
                fig3 = px.line(df_movie_1,
                                x="publishedDate",
                                y="views",
                                title = "Top View Per Day",
                                markers = True,
                                color_discrete_sequence=px.colors.qualitative.Pastel)
                fig3.add_hline(y = overall_avg, 
                                line_color = "#ec5353",
                                line_dash = "dash",
                                annotation_text = f"Overall Mean: {overall_avg:.2f}",
                                annotation_position = "top right")
                st.plotly_chart(fig3, use_container_width = True)

        # two small graphs
        if st.session_state.movies_button:
            col1, col2 = st.columns([3, 2])
            # top 10 video per channel
            with col1:
                mask = df_movie["channelName"].isin([selected_channels]) &\
                        df_movie['duration'].between(min_duration, max_duration) &\
                        df_movie['views'].between(min_views, max_views)
                df_filtered_2 = df_movie[mask]
                top_videos = df_filtered_2.sort_values("views", ascending=False).head(10)
                g2 = px.bar(top_videos, x="views", y="title",
                            title="🔥 Top 10 Videos by View",
                            color="title",
                            color_discrete_sequence = px.colors.qualitative.Pastel)
                g2.update_layout(showlegend=False)
                st.plotly_chart(g2, use_container_width=True)
            
            with col2:
                mask = df_movie["channelName"].isin([selected_channels]) &\
                        df_movie['duration'].between(min_duration, max_duration) &\
                        df_movie['views'].between(min_views, max_views)
                df_filtered_3 = df_movie[mask]
                g3 = px.scatter(df_filtered_3, x="duration", y="views",
                                title="⏳ Duration vs. Views",
                                size="views",
                                color_discrete_sequence = px.colors.qualitative.Pastel)
                g3.update_layout(showlegend=False)
                st.plotly_chart(g3, use_container_width=True)
            
            # table
            if st.session_state.movies_button:
                mask = df_movie["channelName"].isin([selected_channels]) &\
                        df_movie['duration'].between(min_duration, max_duration) &\
                        df_movie['views'].between(min_views, max_views)
                df_filtered_4 = df_movie[mask].drop(columns=["channelName"])

                st.write('📊 Movie Video Dataframe')
                st.dataframe(df_filtered_4)


########################################################################### MUSIC ###############################################################################

with tab4:
    # publishedDate to date
    df_music["publishedDate"] = pd.to_datetime(df_music["publishedDate"]).dt.date

    st.title("🎵 Music")
    # card
    col1, col2, col3 = st.columns(3)
    with col1:
        ttl_video = df_music["title"].count()
        st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}")
    with col2:
        ttl_duration = df_music["duration"].sum()
        st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}")
    with col3: 
        ttl_view = df_music["views"].sum()
        st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}")


    # line: avg view vs. date
    df_music_1 = df_music.groupby("publishedDate")["views"].mean().reset_index()
    overall_avg = df_music["views"].mean()
    g1 = px.line(df_music_1,
                x="publishedDate",
                y="views", 
                title="Monthly Average View",
                color_discrete_sequence=px.colors.qualitative.Pastel)
    # avg line
    g1.add_hline(y = overall_avg, 
                line_color = "#ec5353",
                line_dash = "dash",
                annotation_text = f"Overall Mean: {overall_avg:.2f}",
                annotation_position = "top right")
    st.plotly_chart(g1, use_container_width=True)


    # subplots
    col1, col2 = st.columns(2)

    # small plot left: 時長
    with col1:
            # Top 10 views - Channel
            df_music_2 = df_music.groupby("channelName")["views"].sum().reset_index()
            df_music_2 = df_music_2.sort_values("views", ascending=False)

            st.subheader("📊 Top Views Channel")
            max_channels_views_music = min(len(df_music_2), 20)
            num_channels_views_music = st.slider("📏 Number of Music Channel_views", min_value = 1, max_value = max_channels_views_music, value = 5)
            top_channelview = df_music_2.head(num_channels_views_music)

            g2 = px.bar(top_channelview, x = "views", y = "channelName", orientation = "h",
                  labels = {"views": "Total Views", "channelName": "Channel Name"},
                  title = f"🔥 Channel Video Count Top {num_channels_views_music}", color="channelName",
                  color_discrete_sequence = px.colors.qualitative.Pastel)
            g2.update_layout(showlegend=False)
            st.plotly_chart(g2, use_container_width=True)

    with col2:
        df_music_3 = df_music["channelName"].value_counts().reset_index()
        df_music_3 = df_music_3.sort_values("count", ascending=False)
        df_music_3 = df_music_3.rename(columns={"count":"Num of Video"})

        st.subheader("📊 Top Video Published Channel")
        max_channels_count_music = min(len(df_music_3), 20)
        num_channels_count_music = st.slider("📏 Number of Music Channel_count", min_value = 1, max_value = max_channels_count_music, value = 5)
        top_channels = df_music_3.head(num_channels_count_music)

        g3 = px.bar(top_channels, x = "Num of Video", y = "channelName", orientation = "h",
                labels = {"Num of Video": "Count", "channelName": "Channel Name"},
                title = f"🔥 Channel Video Count Top {num_channels_count_music}", color="channelName",
                color_discrete_sequence = px.colors.qualitative.Pastel)
        g3.update_layout(showlegend=False)
        st.plotly_chart(g3, use_container_width = True)

    ####################################################################################
    # button 
    # def click_button():
        # st.session_state.gaming_button = True
    # button for detailed nalysis
    # st.button('Detailed Analysis', on_click=click_button)
    # 🚀 Music Tab 按鈕
    if st.button("Detailed Analysis - Music", key = "music_analysis"):
        activate_tab("music_button")
        st.session_state.music_button = True
        st.session_state.gaming_button = False
        st.session_state.movies_button = False  # 確保 Movies 相關內容關閉

    if st.session_state.music_button:
        st.subheader("📈 Channel Analysis")
        # select date
        start_date = df_music["publishedDate"].min()
        end_date = df_music["publishedDate"].max()
        options_date = st.sidebar.date_input("Publish Date",
                            (start_date, end_date),
                            start_date,
                            end_date,
                            key = 'music_date')
        # select channel
        df_music_uni_channel = df_music.drop_duplicates("channelName")
        channel_option = df_music_uni_channel.sort_values("channelName", ascending=True)["channelName"]
        options_channel = st.sidebar.selectbox("📌 Music Channel", channel_option)

        # Display a message
        # st.write('Music Trending Video DataFrame')
        # Generate a dataframe and display it in the app
        # st.dataframe(df_music.head(10))

        # views & duration
        with st.sidebar.expander("More Filtering", expanded=False):
            min_views = df_music["views"].min()
            max_views = df_music["views"].max()
            min_views = st.number_input("Min Views", min_value=int(min_views), value=int(min_views))
            max_views = st.number_input("Max Views", max_value=int(max_views), value=int(max_views))

            min_duration = df_music["duration"].min()
            max_duration = df_music["duration"].max()
            min_duration = st.number_input("Min Duration (seconds)", min_value=int(min_duration), value=int(min_duration))
            max_duration = st.number_input("Max Duration (seconds)", max_value=int(max_duration), value=int(max_duration))

        # card
        col1, col2, col3 = st.columns(3)
        with col1:
            mask = df_music["publishedDate"].between(options_date[0], options_date[1]) & df_music["channelName"].isin([options_channel])      
            df_filtered_1 = df_music[mask]
            ttl_video = df_filtered_1["title"].count()
            st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}")
        with col2:
            ttl_duration = df_filtered_1["duration"].sum()
            st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}")
        with col3: 
            ttl_view = df_filtered_1["views"].sum()
            st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}")

        # plot1: top view per day
        if options_date and options_channel:
            mask = df_music["publishedDate"].between(options_date[0], options_date[1]) &\
                    df_music["channelName"].isin([options_channel])
            df_filtered_1 = df_music[mask]

            df_music_1 = df_filtered_1.groupby(["publishedDate", "channelName"])["views"].mean().reset_index()
            g1 = px.line(df_music_1,
                        x= "publishedDate",
                        y= "views",
                        title = "Top View Per Day",
                        markers = True,
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            g1.add_hline(y=overall_avg, 
                         line_color="#ec5353",
                         line_dash="dash",
                         annotation_text=f"Overall Mean: {overall_avg:.2f}",
                         annotation_position="top right")
            st.plotly_chart(g1, use_container_width=True)
                
        if options_date and not options_channel:
            mask = df_music["publishedDate"].between(options_date[0], options_date[1])
            df_filtered_1 = df_music[mask]

            df_music_1 = df_filtered_1.groupby(["publishedDate"])["views"].mean().reset_index()
            g1 = px.line(df_music_1,
                            x="publishedDate",
                            y="views",
                            title = "Top View Per Day",
                            markers = True,
                            color_discrete_sequence=px.colors.qualitative.Pastel)
            g1.add_hline(y=overall_avg, 
                            line_color="#ec5353",
                            line_dash="dash",
                            annotation_text=f"Overall Mean: {overall_avg:.2f}",
                            annotation_position="top right")
            st.plotly_chart(g1, use_container_width=True)

    # two small graphs
    if st.session_state.music_button:
        col1, col2 = st.columns([3, 2])
        # top 10 video per channel
        with col1:
            mask = df_music["channelName"].isin([options_channel]) &\
                    df_music['duration'].between(min_duration, max_duration) &\
                    df_music['views'].between(min_views, max_views)
            df_filtered_2 = df_music[mask]
            top_videos = df_filtered_2.sort_values("views", ascending=False).head(10)
            g2 = px.bar(top_videos, x="views", y="title",
                        title="🔥 Top 10 Videos by View",
                        color="title",
                        color_discrete_sequence = px.colors.qualitative.Pastel)
            g2.update_layout(showlegend=False)
            st.plotly_chart(g2, use_container_width=True)
        
        with col2:
            mask = df_music["channelName"].isin([options_channel]) &\
                    df_music['duration'].between(min_duration, max_duration) &\
                    df_music['views'].between(min_views, max_views)
            df_filtered_3 = df_music[mask]
            g3 = px.scatter(df_filtered_3, x="duration", y="views",
                            title="⏳ Duration vs. Views",
                            size="views",
                            color_discrete_sequence = px.colors.qualitative.Pastel)
            g3.update_layout(showlegend=False)
            st.plotly_chart(g3, use_container_width=True)


    # table
    if st.session_state.music_button:
        mask = df_music["channelName"].isin([options_channel]) &\
                df_music['duration'].between(min_duration, max_duration) &\
                df_music['views'].between(min_views, max_views)
        df_filtered_4 = df_music[mask].drop(columns=["channelName"])

        st.write('📊 Music Video Dataframe')
        st.dataframe(df_filtered_4)


########################################################################### IMPROVEMENT #######################################################################
with tab5:
    st.title("🛠️ Opportunities for Dashboard Enhancement")

    st.markdown("""
    While the current version of the YouTube Dashboard provides a solid foundation for data exploration, 
    there are several areas for potential improvement to enhance functionality, usability, and analytical depth:
    """)

    st.markdown("#### 1. Incomplete Data Coverage")
    st.markdown("""
    The dataset retrieved from Kaggle exhibits gaps in its temporal coverage. 
    Some dates are missing, which may affect the accuracy of time-series analysis. 
    Future versions could incorporate a more complete dataset or implement data imputation methods.
    """)

    st.markdown("#### 2. Channel Comparison Functionality")
    st.markdown("""
    Enable users to select and compare multiple channels within the same time-series chart. 
    This would allow for more intuitive benchmarking of content performance across creators.
    """)

    st.markdown("#### 3. Description-Based Text Analysis")
    st.markdown("""
    Since the dataset contains video descriptions, a new tab can be introduced for 
    Natural Language Processing (NLP) to extract insights from textual content (e.g., keyword trends, topic modeling).
    """)

    st.markdown("#### 4. Viewer Sentiment Analysis")
    st.markdown("""
    If future datasets include user comments or likes/dislikes, sentiment analysis can be applied 
    to better understand audience reactions and their relationship to video performance.
    """)

    st.markdown("#### 5. Predictive Modeling Capabilities")
    st.markdown("""
    Introduce machine learning models (e.g., regression, classification) to predict video success 
    based on metadata such as publish date, video length, or keywords in the description.
    """)

    st.markdown("#### 6. Sidebar Context Management")
    st.markdown("""
    When switching between tabs, the sidebar currently retains filters from previous tabs. 
    Future iterations should dynamically clear or update sidebar components to match the active tab.
    """)
