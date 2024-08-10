<template>
  <div>
    <div class="quote-container mx-auto">
      <p class="quote-text">
        "A book is a gift that you can open again and again." – Garrison Keillor
      </p>
    </div>
    <div class="p-4">
      <table
        class="table table-primary table-hover table-bordered table-responsive align-middle"
      >
        <thead class="table-dark">
          <tr>
            <th>Book Name</th>
            <th>Author</th>
            <th>Section</th>
            <th>Availability</th>
            <th>Request</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.name">
            <td>{{ book[0] }}</td>
            <td>{{ book[1] }}</td>
            <td>{{ book[2] }}</td>
            <td>
              <span v-if="book[3] > 0">Available</span>
              <span v-else>Not Available</span>
            </td>
            <td>
              <button
                type="button"
                @click="requestBook(book[0])"
                :disabled="book[3] <= 0"
                class="btn btn-light"
              >
                Request Book
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      books: [],
    };
  },
  created() {
    this.fetchBooks();
    this.$checkUserRole("user");
  },
  methods: {
    fetchBooks() {
      axios
        .get("http://127.0.0.1:5000/userBooks")
        .then((response) => {
          if(response.status == 200){
            console.log(response.data)
            this.books = response.data.Books;
          }
        })
        .catch((error) => {
          console.error("Error fetching books:", error);
        });
    },
    requestBook(bookName) {
      axios
        .post("http://127.0.0.1:5000/requestBooks", { book: bookName, user:localStorage.getItem('username') })
        .then((response) => {
          alert(response.data.msg);
        })
        .catch((error) => {
          alert("Error: " + error.message);
        });
    },
  },
};
</script>

<style scoped>
.quote-container {
  text-align: center;
  padding: 20px;
  background-color: rgb(13, 13, 13);
  border-bottom: 2px solid #ddd;
  border-top: 2px solid #ddd;
  margin-top: 30px;
  margin-bottom: 20px;
  width: 70%;
}

.quote-text {
  font-size: 1.5em;
  font-style: italic;
  color: #dbdbdb;
}
</style>