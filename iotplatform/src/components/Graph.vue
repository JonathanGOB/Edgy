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
            <b-col>
                <GChart
                        :settings="{ packages: ['corechart', 'gauge'] }"
                        type="Gauge"
                        :data="select"
                        :options="gaugeOptions"
                />
            </b-col>
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
                // eslint-disable-next-line no-console
                console.log(this.$props.sensors)
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