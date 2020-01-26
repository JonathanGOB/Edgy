<template>
    <b-container fluid>
        <b-col>
            <GChart
                    type="LineChart"
                    :data="chartData"
                    :options="chartOptions"
            />
        </b-col>
    </b-container>
</template>

<script>
    export default {
        name: "Graph",
        props: ['value', 'device'],
        data() {
            return {
                items: [],
                chartData: [
                    [],
                    [],
                ],
                chartOptions: {
                    chart: {
                        title: this.$props.device.Name,
                        subtitle: 'sensor data',
                    },
                    hAxis : {
                        textStyle : {
                            fontSize: 10, // or the number you want,
                            format: 'dd/MM/yyyy HH:mm'
                        }

                    }
                }
            }
        },
        methods:{
            calculate(newval){
                this.chartData = [[]]
                this.chartData[0] = ['timestamp', this.$props.device.Name]
                let items = newval

                items.forEach(data => {
                    let row = []
                    row.push(new Date(data.Timestamp))
                    row.push(parseInt(data.Datavalue))
                    this.chartData.push(row)
                })
                // eslint-disable-next-line no-console
                console.log(this.chartData)
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