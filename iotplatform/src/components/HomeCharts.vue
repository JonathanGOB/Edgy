<template>
    <div>
    <GChart
            type="ColumnChart"
            :data="chartData"
            :options="chartOptions"
    />
    </div>
</template>

<script>
    export default {
        name: "HomeCharts"
    }
</script>

<style scoped>

</style>