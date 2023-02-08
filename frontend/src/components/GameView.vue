<template>
    <div class='game-view'>
        <div  class='board'>
            <div class='figures'>
                <img 
                    class='drop-field' 
                    v-for='cell, index in gameData' v-bind:key='cell.id'
                    :alt="cell.figure"
                    :src="require(`../assets/${cell.figure}.svg`)"
                    :draggable='cell.code != 0'
                    :id="'cell'+index"
                    @dragstart='(event) => startDragging(event, index)'
                    @drop='(event) => endDraggingAndMakeTurn(event, index)'>
            </div>
            <img class="board-img" alt='board' src="@/assets/board.svg" draggable='false'>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            gameData: [],
            whiteSided: true,
        }
    },
    computed: {

    },
    methods: {
        convertData() {
            let games = this.$store.getters.games;
            // уточнять какую игру
            let game = games[2];
            let stringData = game['game_data'].split('');
            this.gameData = [];
            for (var i = stringData. length-1; i >= 0; i--) {
            // for (var i = 0; i < stringData.length; i++) {
                let code = stringData[i];
                this.gameData.push(
                    {
                        'id': i,
                        'code': code,
                        'figure': this.getFigureNameByCode(code),
                    }
                )
            }
        },
        getFigureNameByCode(code) {
            switch(code) {
                case '1':
                    return 'pawn-w';
                case '2':
                    return 'rook-w';
                case '3':
                    return 'knight-w';
                case '4':
                    return 'bishop-w';
                case '5':
                    return 'king-w';
                case '6':
                    return 'queen-w';
                case '7':
                    return 'pawn-b';
                case '8':
                    return 'rook-b';
                case '9':
                    return 'knight-b';
                case 'A':
                    return 'bishop-b';
                case 'B':
                    return 'king-b';
                case 'C':
                    return 'queen-b';
                default:
                    return 'empty';
            }
        },
        startDragging(event, index) {
            const cells = document.getElementsByClassName('drop-field');
            for (let i = 0; i < cells.length; i++) {
                cells[i].addEventListener('dragover', (e) => {
                    e.preventDefault();
                });
                cells[i].addEventListener('dragenter', (e) => {
                    e.preventDefault();
                });
            }
            let figure = event.target.getAttribute('alt');
            event.dataTransfer.setData("text/plain", [figure, index]);
            // УДАЛЕНИЕ КАРТИНКИ ИЗ ПРОШЛОГО ПОЛОЖЕНИЯ, ЛУЧШЕ СДЕЛАТЬ ПОСЛЕ БРОСКА ЕЕ В ДРУГУЮ КЛЕТКУ
            this.gameData[index].code = '0';
            this.gameData[index].figure = this.getFigureNameByCode('0');
        },
        endDraggingAndMakeTurn(event, index) {
            let dataTransfered = event.dataTransfer.getData('text').split(',');
            console.log(dataTransfered);
            console.log(index);
            event.target.setAttribute('src', dataTransfered[0])
        },
    },
    name: 'GameView',
    mounted() {
        this.$root.$on('showGame', this.convertData);
        // this.convertData();
    }
}
</script>

<style lang='scss'>

.game-view {
    width: 50%;
    user-select: none;
}

.dragging {
    opacity: 100%;
    cursor: pointer;
}

.board {
    border: 2px solid;
    width: 640px;
    height: 640px;
    position: relative;
    margin-left: auto;
    margin-right: auto;
}
.board-img {
    width: 100%;
}

.figures {
    position: absolute;
    display: grid;
    width: 100%;
    height: 100%;
    grid-template-columns: repeat(8, 80px);
    img {
        width: 100%;
    }
}

@media (max-width: 1280px) {
    .board { 
        width: 480px;
        height: 480px;
    }
}

@media (max-width: 960px) {
    .board { 
        width: 320px;
        height: 320px;
    }
}
</style>