<template>
  <div>
    <el-row>
      <el-col :span="6">
        <div class="block">
          <span class="demonstration">选择城市</span>
          <el-cascader
            v-model="cityId"
            :options="cityOption"
            :props="props"
            @change="handleChange"
          ></el-cascader>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="block">
          <el-date-picker
            v-model="queryDate"
            type="monthrange"
            unlink-panels
            range-separator="至"
            start-placeholder="开始月份"
            end-placeholder="结束月份"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            :shortcuts="shortcuts"
          >
          </el-date-picker>
        </div>
      </el-col>
      <el-col :span="4">
        <el-button type="primary" @click="queryWeather">查询</el-button>
      </el-col>
    </el-row>
    <div class="map">
      <div id="main" style="width: 100%; height: 400px"></div>
    </div>
    <!-- <el-row>
      <WeatherGraph :weatherData="weatherInfo"></WeatherGraph>
    </el-row> -->
  </div>
</template>
<script>
import { cityOptions } from "@/api/citySelectData";
import { queryWeatherInfo } from "@/api/weather_api";
import WeatherGraph from "../components/weather/WeatherGraph.vue";
import * as echarts from "echarts";
export default {
  name: "Weather",
  components: {
    WeatherGraph,
  },
  props: {},
  data() {
    return {
      cityId: 54511,
      queryDate: "",
      cityOption: [],
      shortcuts: [
        {
          text: "本月",
          value: [new Date(), new Date()],
        },
        {
          text: "今年",
          value: () => {
            const end = new Date();
            const start = new Date(new Date().getFullYear(), 0);
            return [start, end];
          },
        },
        {
          text: "过去6个月",
          value: () => {
            const end = new Date();
            const start = new Date();
            start.setMonth(start.getMonth() - 6);
            return [start, end];
          },
        },
      ],
      props: {
        expandTrigger: "hover",
      },
      weatherInfo: [],
      myChart: null,
      option: {
        legend: {},
        tooltip: {
          trigger: "axis",
          axisPointer: { type: "cross" },
        },
        dataset: {
          dimensions: ["日期", "最低温度°", "最高温度°"],
          source: [],
        },
        xAxis: {
          type: "category",
          axisLine: {
            symbol: ["none", "arrow"],
            lineStyle: {
              type: "dashed",
            },
          },
        },
        yAxis: {
          axisLabel: {
            align: "center",
          },
        },
        series: [
          {
            type: "line",
            seriesLayoutBy: "row",
          },
          {
            type: "line",
            seriesLayoutBy: "row",
          },
        ],
      },
    };
  },
  created() {
    this.cityOption = cityOptions();
  },
  mounted() {
    this.echartsInit();
  },
  methods: {
    queryWeather() {
      const query = {
        cityId: this.cityId,
        startDate: this.queryDate[0],
        endDate: this.queryDate[1],
      };
      queryWeatherInfo(query).then((response) => {
        this.weatherInfo = response.data;
        this.updateEcharts();
      });
    },
    handleChange(value) {
      this.cityId = Number(value[value.length - 1]);
    },
    echartsInit() {
      this.myChart = echarts.init(document.getElementById("main"));
      this.myChart.setOption(this.option);
    },
    updateEcharts() {
      this.option.dataset.source = this.weatherInfo;
      this.myChart.setOption(this.option, true);
    },
  },
};
</script>
