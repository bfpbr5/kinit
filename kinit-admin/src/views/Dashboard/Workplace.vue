<script setup lang="ts">
import { ElRow, ElCol, ElSkeleton, ElCard } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { ref, computed, unref } from 'vue'
import { getGreeting, getCurrentDate, getDayOfWeek } from '@/utils'
import avatar from '@/assets/imgs/avatar.jpg'
import { useAuthStore } from '@/store/modules/auth'
import { Dialog } from '@/components/Dialog'
import Write from './components/Write.vue'
import { useRouter } from 'vue-router'
import { PostCreateCase } from '@/api/case'
import { useCaseStore } from '@/store/modules/case'

defineOptions({
  name: 'DashboardWorkplace'
})

const authStore = useAuthStore()
const caseStore = useCaseStore()

const { replace } = useRouter()

const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增案件')
const btnLoading = ref(false)
const saveLoading = ref(false)
const writeRef = ref<ComponentRef<typeof Write>>()

// 新增案件
const createCase = async () => {
  btnLoading.value = true
  dialogVisible.value = true
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  if (formData) {
    saveLoading.value = true
    try {
      const res = await PostCreateCase(formData)
      if (res) {
        btnLoading.value = false
        dialogVisible.value = false
        caseStore.setCaseId(res.data.id)
        replace({ path: '/case/create' })
      }
    } finally {
      saveLoading.value = false
    }
  }
}

const { t } = useI18n()

const user = computed(() => authStore.getUser)
</script>

<template>
  <div class="bg-[var(--app-content-bg-color)] flex-grow">
    <div>
      <ElCard shadow="never">
        <ElSkeleton :loading="loading" animated>
          <ElRow :gutter="20" justify="space-between">
            <ElCol :xl="12" :lg="12" :md="12" :sm="24" :xs="24">
              <div class="flex items-center">
                <img
                  :src="user.avatar ? user.avatar : avatar"
                  alt=""
                  class="w-70px h-70px rounded-[50%] mr-20px"
                />
                <div>
                  <div class="text-20px">
                    {{ getGreeting() }}，{{ user.name }}，{{ t('workplace.happyDay') }}
                  </div>
                  <div class="mt-10px text-14px text-gray-500">
                    {{ getCurrentDate() }}，{{ getDayOfWeek() }}
                  </div>
                </div>
              </div>
            </ElCol>
            <ElCol :xl="12" :lg="12" :md="12" :sm="24" :xs="24">
              <div class="flex h-70px items-center justify-end <sm:mt-20px">
                <div class="px-8px text-right">
                  <div class="text-14px text-gray-400 mb-20px">最近登录时间</div>
                  <span class="text-20px">{{ user.last_login?.split(' ')[0] }}</span>
                </div>
              </div>
            </ElCol>
          </ElRow>
        </ElSkeleton>
      </ElCard>
    </div>
    <div class="mx-20px mt-20px text-right">
      <BaseButton @click="createCase" :loading="btnLoading">新增案件</BaseButton>
    </div>
  </div>

  <Dialog v-model="dialogVisible" :title="dialogTitle" :height="300" width="500px">
    <Write ref="writeRef" />

    <template #footer>
      <BaseButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </BaseButton>
      <BaseButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</BaseButton>
    </template>
  </Dialog>
</template>
