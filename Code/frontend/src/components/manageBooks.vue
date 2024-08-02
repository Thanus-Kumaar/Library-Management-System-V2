<template>
  <div>
    <div
      style="
        text-align: center;
        font-size: 35px;
        padding-bottom: 15px;
        margin-top: 30px;
      "
    >
      Manage Books
    </div>

    <div class="d-flex flex-row">
      <div style="width: 400px; margin-top: 100px">
        <div
          class="d-flex flex-column row-gap-3 mx-auto"
          style="width: max-content"
        >
          <button class="btn btn-light" @click="showModal('addBookModal')">
            Add Book
          </button>
          <button class="btn btn-light" @click="showModal('editBookModal')">
            Edit Book
          </button>
          <button class="btn btn-light" @click="showModal('deleteBookModal')">
            Delete Book
          </button>
        </div>
      </div>
      <div style="flex: 1">
        <div v-if="books.length === 0" class="d-flex flex-fill">
          <h2 class="mx-auto" style="padding: 100px">You have no books</h2>
        </div>
        <div v-else class="p-4">
          <table
            class="table table-primary table-hover table-bordered table-responsive"
          >
            <thead class="table-dark">
              <tr>
                <th>ID</th>
                <th>Book Name</th>
                <th>Author</th>
                <th>Section ID</th>
                <th>No of copies</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="book in books" :key="book.id">
                <td>{{ book.id }}</td>
                <td>{{ book.name }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.sectionID }}</td>
                <td>{{ book.avail }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div
      class="modal fade"
      id="addBookModal"
      tabindex="-1"
      aria-labelledby="addBookModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="background-color: rgb(35, 35, 35)">
          <div class="modal-header">
            <h5 class="modal-title">Add new book</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addBook">
              <div class="mb-3">
                <label for="book" class="form-label">Upload book</label>
                <input
                  type="file"
                  class="form-control"
                  @change="handleFileChange"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="author" class="form-label">Author</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="newBook.author"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="noOfBooks" class="form-label"
                  >Number of books</label
                >
                <input
                  type="text"
                  class="form-control"
                  v-model="newBook.avail"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="secID" class="form-label">Section ID</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="newBook.sectionID"
                  required
                />
              </div>
              <input type="hidden" v-model="isEdit" value="0" />
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Close
                </button>
                <button type="submit" class="btn btn-primary">Add Book</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div
      class="modal fade"
      id="editBookModal"
      tabindex="-1"
      aria-labelledby="editBookModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="background-color: rgb(35, 35, 35)">
          <div class="modal-header">
            <h5 class="modal-title">Edit book</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editBook">
              <div class="mb-3">
                <label for="bookID" class="form-label">Book ID</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="editBookID"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="book2" class="form-label">Upload book</label>
                <input
                  type="file"
                  class="form-control"
                  @change="handleEditFileChange"
                />
              </div>
              <div class="mb-3">
                <label for="author2" class="form-label">Author</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="editBookAuthor"
                />
              </div>
              <div class="mb-3">
                <label for="noOfBooks" class="form-label"
                  >Number of books</label
                >
                <input
                  type="text"
                  class="form-control"
                  v-model="editBookAvail"
                />
              </div>
              <div class="mb-3">
                <label for="secID2" class="form-label">Section ID</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="editBookSectionID"
                />
              </div>
              <input type="hidden" v-model="isEditEdit" value="1" />
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Close
                </button>
                <button type="submit" class="btn btn-primary">Edit Book</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div
      class="modal fade"
      id="deleteBookModal"
      tabindex="-1"
      aria-labelledby="deleteBookModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="background-color: rgb(35, 35, 35)">
          <div class="modal-header">
            <h5 class="modal-title">Delete Book</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="deleteBook">
              <div class="mb-3">
                <label for="bookID2" class="form-label">Book ID</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="deleteBookID"
                  required
                />
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Close
                </button>
                <button type="submit" class="btn btn-primary">
                  Delete Book
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      books: [], // Books data
      newBook: {
        file: null,
        author: "",
        avail: "",
        sectionID: "",
      },
      editBookID: "",
      editBookFile: null,
      editBookAuthor: "",
      editBookAvail: "",
      editBookSectionID: "",
      deleteBookID: "",
      isEdit: "0",
      isEditEdit: "1",
    };
  },
  methods: {
    fetchBooks() {
      axios
        .get("http://127.0.0.1:5000/manageBooks")
        .then((response) => {
          this.books = response.data.books;
        })
        .catch((error) => {
          console.error("Error fetching books:", error);
        });
    },
    showModal(modalId) {
      const modal = new bootstrap.Modal(document.getElementById(modalId));
      modal.show();
    },
    handleFileChange(event) {
      this.newBook.file = event.target.files[0];
    },
    handleEditFileChange(event) {
      this.editBookFile = event.target.files[0];
    },
    addBook() {
      const formData = new FormData();
      if (this.newBook.file) {
        formData.append("book", this.newBook.file);
      }
      formData.append("author", this.newBook.author);
      formData.append("noOfBooks", this.newBook.avail);
      formData.append("secID", this.newBook.sectionID);
      formData.append("isEdit", this.isEdit);
      axios
        .post("http://127.0.0.1:5000/manageBooks", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          this.fetchBooks();
          this.newBook = { file: null, author: "", avail: "", sectionID: "" };
          const modal = new bootstrap.Modal(
            document.getElementById("addBookModal")
          );
          modal.hide();
        })
        .catch((error) => {
          console.error("Error adding book:", error);
        });
    },
    editBook() {
      const formData = new FormData();
      formData.append("bookID", this.editBookID);
      formData.append("book", this.editBookFile);
      formData.append("author", this.editBookAuthor);
      formData.append("noOfBooks", this.editBookAvail);
      formData.append("secID", this.editBookSectionID);
      formData.append("isEdit", this.isEditEdit);

      axios
        .post("http://127.0.0.1:5000/manageBooks", formData)
        .then((response) => {
          this.fetchBooks(); // Refresh the book list
          this.editBookID = "";
          this.editBookFile = null;
          this.editBookAuthor = "";
          this.editBookAvail = "";
          this.editBookSectionID = "";
          document.getElementById("editBookModal").modal("hide");
        })
        .catch((error) => {
          console.error("Error editing book:", error);
        });
    },
    deleteBook() {
      axios
        .delete(`http://127.0.0.1:5000/manageBooks?bookID=${this.deleteBookID}`)
        .then((response) => {
          this.fetchBooks(); // Refresh the book list
          this.deleteBookID = "";
          document.getElementById("deleteBookModal").modal("hide");
        })
        .catch((error) => {
          console.error("Error deleting book:", error);
        });
    },
  },
  mounted() {
    this.fetchBooks();
  },
};
</script>
