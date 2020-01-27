<template>
    <b-container fluid>
        <b-col>
            <GChart
                    type="LineChart"
                    :data="chartData"
                    :options="chartOptions"
            />
        </b-col>
        <b-row>
        </b-row>
    </b-container>
</template>

<script>
    export default {
        name: "Graph",
        props: ['value', 'device', 'sensors'],
        data() {
            return {
                items: [],
                select: [],
                chartData: [
                    [],
                    [],
                ],

                gaugeOptions: {
                    width: 400, height: 120,
                    redFrom: 90, redTo: 100,
                    yellowFrom: 75, yellowTo: 90,
                    minorTicks: 5
                },

                chartOptions: {
                    chart: {
                        title: this.$props.device.Name,
                        subtitle: 'sensor data',
                    },
                    hAxis: {
                        textStyle: {
                            fontSize: 10, // or the number you want,
                            format: 'dd/MM/yyyy HH:mm'
                        }

                    }
                }
            }
        },
        methods: {
            calculate(newval) {
                if (!this.$props.sensors) {
                    this.chartData = [[]]
                    this.chartData[0] = ['timestamp', this.$props.device.Name]
                    let items = newval

                    items.forEach(data => {
                        let row = []
                        row.push(new Date(data.Timestamp))
                        row.push(parseInt(data.Datavalue))
                        this.chartData.push(row)
                    })

                    this.select = [[]]
                    this.select[0] = ['Label', 'Value']

                    this.select.push([this.$props.device.Name, parseInt(items[items.length - 1].Datavalue)])
                } else if (this.$props.sensors) {
                    let timeline = []
                    newval.forEach((data, index) => {
                        if (index > 0 && data.Timestamp != timeline[index - 1]) {
                            timeline.push(data.Timestamp)
                        }

                        if (index == 0) {
                            timeline.push(data.Timestamp)
                        }
                    })

                    let sensors = []

                    newval.forEach(data => {
                        this.$props.sensors.forEach(sensor => {
                            if(data.PartitionKey == sensor.ConnectionString){
                                if(!this.findTrue(sensor.ConnectionString, sensors)){
                                    sensors.push(sensor.ConnectionString)
                                }
                            }
                        })
                    })

                    let data_array = [];

                    timeline.forEach(() => {
                        let null_array = []
                        sensors.forEach(() => {
                            null_array.push(null)
                        })
                        data_array.push(null_array)
                    })

                    let id = 0
                    newval.forEach((data, index) => {
                        if (timeline[id] == data.Timestamp) {
                            let column = this.search(data.PartitionKey, sensors)
                            data_array[id][column] = parseInt(data.Datavalue)
                        }

                        if (timeline.length - 1 != id && index != newval.length - 1) {
                            if (timeline[id] != newval[index + 1]) {
                                id++
                            }
                        }
                    })

                    let sensor_names = []
                    newval.forEach(data => {
                        this.$props.sensors.forEach(sensor => {
                            if(data.PartitionKey == sensor.ConnectionString){
                                if(!this.findTrue(sensor.Name, sensor_names)){
                                    sensor_names.push(sensor.Name)
                                }
                            }
                        })
                    })

                    sensor_names.unshift('timestamp')
                    data_array.forEach((data, index) => {
                        data.unshift(new Date(timeline[index]))
                    })

                    data_array.unshift(sensor_names)

                    this.chartData = data_array
                }
            },

            search(value, array) {
                for (var i = 0; i < array.length; i++) {
                    if (array[i] === value) {
                        return i
                    }
                }
            },

            findTrue(value, array) {
                for (var i = 0; i < array.length; i++) {
                    if (array[i] === value) {
                        return true
                    }
                }

                return false
            }
        },

        watch: {
            value: {
                // eslint-disable-next-line no-unused-vars
                handler(newval, oldval) {
                    this.calculate(newval)
                }
            }
        }
    }
</script>

<style scoped>

</style>