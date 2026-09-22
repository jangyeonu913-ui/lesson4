import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

# 제목 설정
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 열 전처리: 세로막대 기호(|)로 여러 개 적힌 경우 첫 번째 장르만 추출
    df["genre"] = df["genre"].astype(str).str.split("|").str[0]

    return df


# 데이터 로드
df = load_data()

# ---------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
st.header("1. 장르별 영화 편수 분포")

# 장르별 영화 수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts,
    values="count",
    names="genre",
    hole=0.4,
    title="장르별 영화 편수 비율",
)

# 마우스 호버 시 편수(value)와 비율(percent) 표시 설정
fig_donut.update_traces(
    hoverinfo="label+value+percent", textinfo="label+percent"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_donut, use_container_width=True)

# 구분선 및 분석 설명 구역
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("구현하고 싶으신 분석 결과를 여기에 한 문장으로 작성해주세요.")
st.markdown("---")

# ---------------------------------------------------------
# 두 번째 그래프: 장르별/영화별 총 관객 수 (트리맵)
# ---------------------------------------------------------
st.header("2. 장르 및 영화별 총 관객 수 트리맵")

# Plotly 트리맵 생성 (계층 구조: 장르 -> 영화명)
fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체 장르"), "genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객 수 분포",
    hover_data={"total_audi": ":,d"},
)

# 마우스 호버 시 영화명과 총 관객 수 표시 설정
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,}명<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_treemap, use_container_width=True)

# 구분선 및 분석 설명 구역
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("구현하고 싶으신 분석 결과를 여기에 한 문장으로 작성해주세요.")
st.markdown("---")

# ---------------------------------------------------------
# 세 번째 그래프: 총 관객 수 히스토그램
# ---------------------------------------------------------
st.header("3. 총 관객 수 분포 (히스토그램)")

# Plotly 히스토그램 생성
fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객 수 분포",
    labels={"total_audi": "총 관객 수"},
    color_discrete_sequence=["#636EFA"],
)

fig_hist.update_layout(
    xaxis_title="총 관객 수 (명)",
    yaxis_title="영화 수 (편)",
    bargap=0.1,
)

fig_hist.update_traces(
    hovertemplate="관객 수 구간: %{x}<br>영화 수: %{y}편<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_hist, use_container_width=True)

# 데이터 자동 분석 정보 계산
max_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = max_movie["movieNm"]
top_movie_audi = max_movie["total_audi"]

# 관객 수가 가장 많이 몰려 있는 구간 계산 (200만 명 단위 구간)
bin_size = 2000000
df["audi_bin"] = (df["total_audi"] // bin_size) * bin_size
most_frequent_bin = df["audi_bin"].mode()[0]
most_frequent_count = (df["audi_bin"] == most_frequent_bin).sum()

bin_start = f"{int(most_frequent_bin):,}"
bin_end = f"{int(most_frequent_bin + bin_size):,}"

# 구분선 및 분석 설명 구역
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write(
    f"대부분의 영화({most_frequent_count}편)가 관객 수 **{bin_start}명 ~ {bin_end}명** 구간에 집중되어 있으며, "
    f"가장 많은 관객을 동원한 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,}명)입니다."
)
st.markdown("---")

# ---------------------------------------------------------
# 네 번째 그래프: 개봉일 스크린 수 vs 총 관객 수 (산점도)
# ---------------------------------------------------------
st.header("4. 개봉일 스크린 수와 총 관객 수의 관계 (산점도)")

# Plotly 산점도 생성
fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수 vs 총 관객 수",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르",
    },
    hover_data={"first_scrn": ":,d", "total_audi": ":,d", "genre": True},
)

fig_scatter.update_layout(
    xaxis_title="개봉일 스크린 수 (개)",
    yaxis_title="총 관객 수 (명)",
)

# 마우스 호버 커스텀 설정
fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,}명<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_scatter, use_container_width=True)

# 구분선 및 분석 설명 구역
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write(
    "개봉일 스크린 수가 많을수록 대체로 총 관객 수도 증가하는 양의 상관관계를 보이며, 장르별 스크린 확보 및 관객 수 분포 특징을 확인할 수 있습니다."
)
st.markdown("---")
