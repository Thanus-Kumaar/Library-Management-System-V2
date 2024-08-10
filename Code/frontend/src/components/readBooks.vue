<template>
  <div>
    <div class="p-4">
      <h2 class="text-center mb-4">Read your e-books here</h2>
      <div
        v-if="books.length == 0"
        class="text-center"
        style="margin-top: 200px"
      >
        Borrow or request books first to read them!
      </div>
      <table
        class="table table-primary table-hover table-bordered table-responsive align-middle"
        v-if="books.length != 0"
      >
        <thead class="table-dark">
          <tr>
            <th>Book Name</th>
            <th>Author</th>
            <th>Section</th>
            <th>Read</th>
            <th>Return</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(book, index) in books" :key="index">
            <td>{{ book[0] }}</td>
            <td>{{ book[1] }}</td>
            <td>{{ book[2] }}</td>
            <td>
              <button
                type="button"
                @click="this.$router.push(`/view-file?book=${book[0]}`)"
                class="btn btn-light"
              >
                Read Book
              </button>
            </td>
            <td>
              <button
                type="button"
                @click="returnBook(book[0])"
                class="btn btn-light"
              >
                Return Book
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
  methods: {
    returnBook(bookName) {
      axios
      .post("http://127.0.0.1:5000/returnBook", {
        user:localStorage.getItem('username'),
        book: bookName,
      })
      .then((response) => {
        if (response.status == 200) {
          this.fetchBooks();
        }
      });
    },
    fetchBooks(){
      axios
      .get("http://127.0.0.1:5000/readBooks", {
        params: {
          user: localStorage.getItem("username"),
        },
      })
      .then((response) => {
        if (response.status == 200) {
          console.log(response.data);
          this.books = response.data.books;
        }
      });
    }
  },
  created() {
    this.$checkUserRole("user");
    this.fetchBooks();
  },
};
</script>
