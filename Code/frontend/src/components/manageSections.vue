<template>
  <div>
    <div style="text-align: center; font-size: 35px; padding-bottom: 15px; margin-top: 30px;">
      Manage Sections
    </div>
    <div class="d-flex flex-row">
      <div style="width: 400px; margin-top: 100px;">
        <div class="d-flex flex-column row-gap-3 mx-auto" style="width: max-content;">
          <button class="btn btn-light" type="button" @click="showModal('addSection')">
            Add Section
          </button>
          <button class="btn btn-light" type="button" @click="showModal('editSection')">
            Edit Section
          </button>
          <button class="btn btn-light" type="button" @click="showModal('deleteSection')">
            Delete Section
          </button>
        </div>
      </div>
      <div style="flex: 1;">
        <div v-if="sections.length === 0" class="d-flex flex-fill">
          <h2 class="mx-auto" style="padding: 100px;">You have no sections</h2>
        </div>
        <div v-else class="p-4">
          <table class="table table-primary table-hover table-bordered table-responsive">
            <thead class="table-dark">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th>Creation Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(section, index) in sections" :key="index">
                <td>{{ section.id }}</td>
                <td>{{ section.name }}</td>
                <td>{{ section.description }}</td>
                <td>{{ section.creationDate }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="modal fade" tabindex="-1" id="addSectionModal" v-show="modals.addSection">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="background-color: rgb(35, 35, 35);">
          <div class="modal-header">
            <h5 class="modal-title">Add new section</h5>
            <button type="button" class="btn-close" @click="hideModal('addSection')" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addSection">
              <div class="mb-3">
                <label for="sectionName" class="form-label">Section Name</label>
                <input type="text" class="form-control" v-model="newSection.name" required>
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <input type="text" class="form-control" v-model="newSection.description" required>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="hideModal('addSection')">Close</button>
                <button type="submit" class="btn btn-primary">Add Section</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" tabindex="-1" id="editSectionModal" v-show="modals.editSection">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="background-color: rgb(35, 35, 35);">
          <div class="modal-header">
            <h5 class="modal-title">Edit section</h5>
            <button type="button" class="btn-close" @click="hideModal('editSection')" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editSection">
              <div class="mb-3">
                <label for="secID" class="form-label">Section ID</label>
                <input type="text" class="form-control" v-model="sectionToEdit.id" required>
              </div>
              <div class="mb-3">
                <label for="sectionName" class="form-label">Section Name</label>
                <input type="text" class="form-control" v-model="sectionToEdit.name" required>
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <input type="text" class="form-control" v-model="sectionToEdit.description" required>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="hideModal('editSection')">Close</button>
                <button type="submit" class="btn btn-primary">Edit Section</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" tabindex="-1" id="deleteSectionModal" v-show="modals.deleteSection">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="background-color: rgb(35, 35, 35);">
          <div class="modal-header">
            <h5 class="modal-title">Delete section</h5>
            <button type="button" class="btn-close" @click="hideModal('deleteSection')" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="deleteSection">
              <div class="mb-3">
                <label for="secID" class="form-label">Section ID</label>
                <input type="text" class="form-control" v-model="sectionToDelete.id" required>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="hideModal('deleteSection')">Close</button>
                <button type="submit" class="btn btn-primary">Delete Section</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      sections: [],
      modals: {
        addSection: false,
        editSection: false,
        deleteSection: false
      },
      newSection: {
        name: '',
        description: ''
      },
      sectionToEdit: {
        id: '',
        name: '',
        description: ''
      },
      sectionToDelete: {
        id: ''
      }
    };
  },
  methods: {
    showModal(modalId) {
      this.modals[modalId] = true;
      const modalElement = document.getElementById(modalId + 'Modal');
      if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
      }
    },
    hideModal(modalId) {
      this.modals[modalId] = false;
      const modalElement = document.getElementById(modalId + 'Modal');
      if (modalElement) {
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) {
          modal.hide();
        }
      }
    },
    async addSection() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/manageSections', this.newSection);
        if(response.status == 200){
          this.hideModal('addSection');
          this.newSection = { name: '', description: '' };
          this.fetchSections();
        }
      } catch (error) {
        alert('Error adding section');
      }
    },
    async editSection() {
      try {
        await axios.put('http://127.0.0.1:5000/manageSections', this.sectionToEdit);
        this.hideModal('editSection');
        this.sectionToEdit = { id: '', name: '', description: '' };
        this.fetchSections(); // Reload sections
      } catch (error) {
        alert('Error editing section');
      }
    },
    async deleteSection() {
      try {
        await axios.delete('http://127.0.0.1:5000/manageSections', {
          params: { secID: this.sectionToDelete.id }
        });
        this.hideModal('deleteSection');
        this.sectionToDelete = { id: '' };
        this.fetchSections(); // Reload sections
      } catch (error) {
        alert('Error deleting section');
      }
    },
    async fetchSections() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/manageSections');
        if(response.status === 200) {
          const sectionsData = response.data.sections;
          this.sections = sectionsData.map(section => ({
            id: section[0],
            name: section[1],
            creationDate: section[2],
            description: section[3]
          }));
        }
      } catch (error) {
        alert('Error fetching sections');
      }
    }
  },
  created() {
    this.fetchSections();
  }
};
</script>
