<template>
  <div>
    <v-data-table :headers="headers" :items="items" :loading="loading">
      <template #item.case_priority.name="{ item }">
        <case-priority :priority="item.case_priority.name" />
      </template>
      <template #item.status="{ item }">
        <case-status :status="item.status" :id="item.id" />
      </template>
      <template #item.project.name="{ item }">
        <v-chip small :color="item.project.color" text-color="white">
          {{ item.project.name }}
        </v-chip>
      </template>
      <template #item.reported_at="{ item }">
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <span v-bind="attrs" v-on="on">{{ item.reported_at | formatRelativeDate }}</span>
          </template>
          <span>{{ item.reported_at | formatDate }}</span>
        </v-tooltip>
      </template>
      <template #item.data-table-actions="{ item }">
        <v-menu bottom left>
          <template #activator="{ on }">
            <v-btn icon v-on="on">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item :to="{ name: 'CaseTableEdit', params: { name: item.name } }">
              <v-list-item-title>View / Edit</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-data-table>
  </div>
</template>
<script>
import { mapActions } from "vuex"

import CasePriority from "@/case/priority/CasePriority.vue"
import CaseStatus from "@/case/CaseStatus.vue"

export default {
  name: "CaseSummaryTable",

  components: {
    CasePriority,
    CaseStatus,
  },

  data() {
    return {
      headers: [
        { text: "Name", value: "name", align: "left", sortable: false, width: "10%" },
        { text: "Title", value: "title", sortable: false },
        { text: "Status", value: "status", sortable: false },
        { text: "Type", value: "case_type.name", sortable: false },
        { text: "Priority", value: "case_priority.name", sortable: false, width: "10%" },
        { text: "Project", value: "project.name", sortable: false },
        { text: "Reported At", value: "reported_at", sortable: false },
        { text: "Assignee", value: "assignee.email", sortable: false },
        { text: "", value: "data-table-actions", sortable: false, align: "end" },
      ],
    }
  },

  props: {
    items: {
      default: function () {
        return []
      },
      type: Array,
    },
    loading: {
      default: function () {
        return false
      },
      type: [String, Boolean],
    },
  },

  methods: {
    ...mapActions("case", ["showEditSheet"]),
  },
}
</script>
