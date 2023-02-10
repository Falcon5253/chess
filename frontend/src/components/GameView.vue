<template>
    <div class='game-view'>
        <div  class='board'>
            <div class='figures'>
                <img 
                    class='drop-field' 
                    v-for='cell, index in gameData' v-bind:key='cell.id'
                    :alt="cell.figure"
                    :src="require(`../assets/${cell.figure}.svg`)"
                    :draggable='cell.figure != "empty" && !isTurnMade'
                    :id="cell.cell"
                    @dragstart='(event) => startDragging(event, index)'
                    @drop='(event) => endDraggingAndMakeTurn(event, index)'>
            </div>
            <img class="board-img" alt='board' src="@/assets/board.svg" draggable='false'>
            <input
                class='commit-turn'
                type="button"
                value='Поддвердить ход'
                :disabled='!isTurnMade'
                @click='sendTurnData()'>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            gameId: -1,
            whiteSided: true,
            isTurnMade: false,
            turn: '',
        }
    },
    computed: {
        gameData() {
            if (this.gameId != -1 && this.game != undefined) {
                return this.game['game_data'];
            }
            return []
        },
        game() {
            return this.$store.getters.games.find(element => element.id == this.gameId);
        }
    },
    methods: {
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
            let figure = this.gameData[index].figure;
            event.dataTransfer.setData("text/plain", [figure, index]);
        },
        endDraggingAndMakeTurn(event, index) {
            // Getting data from previous cell
            let dataTransfered = event.dataTransfer.getData('text').split(',');
            console.log(dataTransfered);
            let figure = dataTransfered[0];
            let previousCellIndex = dataTransfered[1];
            
            // Editing game data
            this.gameData[previousCellIndex].figure = 'empty';
            this.gameData[index].figure = figure;
            this.game['game_data'] = this.gameData;
            
            // Creating turn for server request
            let from = this.gameData[previousCellIndex].cell;
            let to = this.gameData[index].cell;
            this.turn = from + "-" + to;
            this.isTurnMade = true;
        },
        sendTurnData() {
            console.log(this.gameData);
            // Нормализовать данные для сервера и отправить их

            console.log(this.turn);
            
        }
    },
    name: 'GameView',
    mounted() {
        this.$root.$on('showGame', (gameId) => this.gameId = gameId);

        // Checking if gameId in path and getting it from there
        if (!isNaN(parseInt(this.$route.params.id))) {
            this.gameId = this.$route.params.id;
        }
    },
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

.commit-turn {
    margin-top: 15px;
    width: 100%;    
    height: 60px;
}

.commit-turn:disabled {
    display: none;
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