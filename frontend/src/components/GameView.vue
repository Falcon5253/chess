<template>
    <div class='game-view'>
        <img class='board' alt="board" src="../assets/board.svg" draggable='false'>
    </div>
</template>

<script>
export default {
  name: 'GameView',
}
</script>

<style lang='scss'>

.game-view {
    width: 50%;
    user-select: none;
}

.board {
    border: 2px solid;
    width: 640px;
}

@media (max-width: 1280px) {
    .board { 
        width: 480px;
    }
}

@media (max-width: 960px) {
    .board { 
        width: 320px;
    }
}
</style>