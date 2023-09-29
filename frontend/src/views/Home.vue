<template>
  <div class="home">
    <Intro/>
  </div>
</template>

<script>
// @ is an alias to /src
import Intro from '@/components/Intro.vue'

export default {
  name: 'Home',
  components: {
    Intro
  }
}
</script>
