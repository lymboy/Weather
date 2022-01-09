<template>
  <div>
    <vue-echarts :option="option" style="height: 500px" ref="chart" />
  </div>
</template>

<script>
import { VueEcharts } from "vue3-echarts";
export default {
  name: "WeatherGraph",
  props: {
    weatherData: Array,
  },
  components: {
    VueEcharts,
  },
  data() {
    return {
      option: {
        legend: {},
        tooltip: {},
        dataset: {
          source: this.weatherData,
        },
        xAxis: {
          type: "category",
        },
        yAxis: {},
      },
    };
  },
  created() {
    //   this.$refs.chart.refreshOption();
  },
  mounted() {
    console.log(JSON.stringify(this.weatherData));
  }, //在Chart.vue中加入watch
  watch: {
    //观察option的变化
    option: {
      handler(newVal, oldVal) {
        if (this.chart) {
          if (newVal) {
            this.chart.setOption(newVal);
          } else {
            this.chart.setOption(oldVal);
          }
        } else {
          this.init();
        }
      },
      deep: true, //对象内部属性的监听，关键。
    },
  },
};
</script>

<style></style>
