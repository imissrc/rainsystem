<template>
  <HistoryImageEnhance name="去雨" :task-type="taskType" />
</template>

<script>
import { taskType } from '@/utils/constants'
import HistoryImageEnhance from '@/components/imageEnhance/historyImageEnhance'
export default {
  name: 'HistoryImageDerain',
  components: { HistoryImageEnhance },
  data() {
    return {
      taskType: taskType.imageDeraining
    }
  }
}
</script>

<style scoped>

</style>
