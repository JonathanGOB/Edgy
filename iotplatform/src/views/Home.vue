<template>
  <div class="home">
    <Sidebar>
    </Sidebar>
  </div>
</template>

<script>
// @ is an alias to /src
//import HelloWorld from '@/components/HelloWorld.vue'
import Sidebar from "../components/Sidebar";

export default {
  name: 'home',
  created() {
    if(!this.$store.getters.user){
      this.$router.push('/login')
    }
  },
  components: {
    Sidebar

  }
}
</script>
