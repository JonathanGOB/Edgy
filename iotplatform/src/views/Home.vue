<template>
  <div class="home">

  </div>
</template>

<script>
// @ is an alias to /src
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
  created() {
    if(!this.$store.getters.user){
      this.$router.push('/login')
    }
  },
  components: {

  }
}
</script>
