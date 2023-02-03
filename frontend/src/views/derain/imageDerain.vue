<template>
  <ImageEnhance name="去雨" :task-type="taskType" />
</template>

<script>
import ImageEnhance from '@/components/imageEnhance/imageEnhance'
import { taskType } from '@/utils/constants'

export default {
  name: 'ImageDerain',
  components: {
    ImageEnhance
  },
  data() {
    return {
      taskType: taskType.imageDeraining
    }
  }
}
</script>

<style scoped>
</style>
