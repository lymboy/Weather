import request from "@/utils/request";

// 查询职工信息列表
export function queryWeatherInfo(query) {
    return request({
        url: '/weather/get_weather_info_between',
        method: 'get',
        params: query
    })
}