<template>
    <img
        :alt="cell.figure"
        :src="require(`../../assets/${cell.figure}.svg`)"
        :draggable='cell.figure != "empty" && !isTurnMade && !waitingForOpponent'
        :id="cell.cell"
        @dragover='(e) => e.preventDefault()'
        @dragenter='(e) => e.preventDefault()'
        @dragstart='(e) => startDragging(e)'
        @drop='(e) => endDragging(e)'
>
</template>

<script>

export default {
    name: 'CellBlock',
    props: ['cell', 'index', 'isTurnMade', 'waitingForOpponent'],
    mounted() {
    },
    methods: {
        startDragging(event) {
            let figure = this.cell.figure;
            event.dataTransfer.setData("text/plain", [figure, this.index]);
        },
        endDragging(event) {
            let turnData = event.dataTransfer.getData('text') + "," + (this.index);
            this.$emit('makeTurn', turnData);
        }
    }
}

</script>

<style lang='scss'>

</style>
