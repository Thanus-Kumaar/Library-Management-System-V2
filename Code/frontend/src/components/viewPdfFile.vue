<template>
  <div style="width: 100%; height: 85vh; margin-top: 10px;">
    <object
      v-if="pdfUrl"
      :data="pdfUrl"
      type="application/pdf"
      style="width: 100%; height: 100%"
      width="800"
      height="1000"
    >
      <p>
        Your browser does not support PDFs.
        <a :href="pdfUrl">Download the PDF</a>.
      </p>
    </object>
    <p v-else>Loading...</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PdfViewer",
  data() {
    return {
      pdfUrl: null,
    };
  },
  created() {
    this.loadPdf();
    this.$checkUserRole("user");
  },
  methods: {
    async loadPdf() {
      const filename = this.$route.query.book;
      console.log(filename);
      if (filename) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/view-file`, {
            params: { filename },
            responseType: "blob",
            headers: {
              "Cache-Control": "no-cache",
              Pragma: "no-cache",
            },
          });
          const url = window.URL.createObjectURL(
            new Blob([response.data], { type: "application/pdf" })
          );
          this.pdfUrl = url;
        } catch (error) {
          console.error("Error loading PDF:", error);
        }
      }
    },
  },
};
</script>
