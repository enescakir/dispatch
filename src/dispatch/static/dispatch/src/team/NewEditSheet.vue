<template>
  <ValidationObserver v-slot="{ invalid, validated }">
    <v-navigation-drawer v-model="showCreateEdit" app clipped right width="500">
      <template #prepend>
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title v-if="id" class="title"> Edit </v-list-item-title>
            <v-list-item-title v-else class="title"> New </v-list-item-title>
            <v-list-item-subtitle>Team</v-list-item-subtitle>
          </v-list-item-content>
          <v-btn
            icon
            color="info"
            :loading="loading"
            :disabled="invalid || !validated"
            @click="save()"
          >
            <v-icon>save</v-icon>
          </v-btn>
          <v-btn icon color="secondary" @click="closeCreateEdit()">
            <v-icon>close</v-icon>
          </v-btn>
        </v-list-item>
      </template>
      <v-card flat>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <span class="subtitle-2">Details</span>
              </v-flex>
              <v-flex xs12>
                <ValidationProvider name="Name" rules="required" immediate>
                  <v-text-field
                    v-model="name"
                    slot-scope="{ errors, valid }"
                    :error-messages="errors"
                    :success="valid"
                    label="Name"
                    hint="A name for your team."
                    clearable
                    required
                  />
                </ValidationProvider>
              </v-flex>
              <v-flex xs12>
                <ValidationProvider name="Email" rules="required" immediate>
                  <v-text-field
                    v-model="email"
                    slot-scope="{ errors, valid }"
                    label="Email"
                    :error-messages="errors"
                    :success="valid"
                    hint="The team's email."
                    clearable
                    required
                  />
                </ValidationProvider>
              </v-flex>
              <v-flex xs12>
                <ValidationProvider name="Company" immediate>
                  <v-text-field
                    v-model="company"
                    slot-scope="{ errors, valid }"
                    label="Company"
                    :error-messages="errors"
                    :success="valid"
                    hint="The team's company."
                    clearable
                  />
                </ValidationProvider>
              </v-flex>
              <v-flex xs12>
                <span class="subtitle-2"
                  >Engagement
                  <v-tooltip max-width="250px" bottom>
                    <template #activator="{ on, attrs }">
                      <v-icon v-bind="attrs" v-on="on"> help_outline </v-icon>
                    </template>
                    This team will be automatically engaged for any incident or case matching the
                    following filters.
                  </v-tooltip>
                </span>
              </v-flex>
              <v-flex xs12>
                <search-filter-combobox
                  v-model="filters"
                  :project="project"
                  label="Filters"
                  hint="Select one or more filters that will determine when a team is engaged."
                />
              </v-flex>
              <v-flex xs12>
                <span class="subtitle-2"
                  >Evergreen
                  <v-tooltip max-width="250px" bottom>
                    <template #activator="{ on, attrs }">
                      <v-icon v-bind="attrs" v-on="on"> help_outline </v-icon>
                    </template>
                    Dispatch will send the owner a reminder email to the resource owner, reminding
                    them to keep the resource current.
                  </v-tooltip>
                </span>
              </v-flex>
              <v-flex xs12>
                <ValidationProvider name="Owner" immediate>
                  <v-text-field
                    v-model="evergreen_owner"
                    slot-scope="{ errors, valid }"
                    label="Owner"
                    :error-messages="errors"
                    :success="valid"
                    hint="Owner of this team."
                    clearable
                  />
                </ValidationProvider>
              </v-flex>
              <v-flex xs12>
                <ValidationProvider name="Reminder Interval" immediate>
                  <v-text-field
                    v-model="evergreen_reminder_interval"
                    slot-scope="{ errors, valid }"
                    label="Reminder Interval"
                    :error-messages="errors"
                    :success="valid"
                    type="number"
                    hint="Number of days that should elapse between reminders sent to the team owner."
                    placeholder="90"
                    clearable
                    min="1"
                  />
                </ValidationProvider>
              </v-flex>
              <v-flex xs12>
                <v-checkbox
                  v-model="evergreen"
                  hint="Enabling evergreen will send periodic reminders to the owner to update this team."
                  label="Enabled"
                />
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>
  </ValidationObserver>
</template>

<script>
import { mapFields } from "vuex-map-fields"
import { mapActions } from "vuex"
import { ValidationObserver, ValidationProvider, extend } from "vee-validate"
import { required } from "vee-validate/dist/rules"
import SearchFilterCombobox from "@/search/SearchFilterCombobox.vue"

extend("required", {
  ...required,
  message: "This field is required",
})

export default {
  name: "ServiceNewEditSheet",

  data() {
    return {
      visibilities: ["Open"],
    }
  },

  components: {
    ValidationObserver,
    ValidationProvider,
    SearchFilterCombobox,
  },

  computed: {
    ...mapFields("team", [
      "selected.name",
      "selected.company",
      "selected.email",
      "selected.filters",
      "selected.project",
      "selected.evergreen_owner",
      "selected.evergreen",
      "selected.evergreen_reminder_interval",
      "selected.id",
      "selected.loading",
      "dialogs.showCreateEdit",
    ]),
    ...mapFields("route", ["query"]),
  },

  methods: {
    ...mapActions("team", ["save", "closeCreateEdit"]),
  },

  created() {
    if (this.query.project) {
      this.project = { name: this.query.project }
    }
  },
}
</script>
