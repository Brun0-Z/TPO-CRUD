const { createApp } = Vue;
createApp({
  data() {
    return {
      canchas: [],
      url: "https://vrunn0.pythonanywhere.com/cancha", // si ya lo subieron a pythonanywhere
      error: false,
      cargando: true,
      /*atributos para el guardar los valores del formulario */
      id: 0,
      nombre: "",
      imagen: "",
      tipo: 0,
      precio: 0,
    };
  },
  methods: {
    fetchData(url) {
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          this.canchas = data;
          this.cargando = false;
        })
        .catch((err) => {
          console.error(err);
          this.error = true;
        });
    },
    eliminar(cancha) {
      const url = this.url + "/" + cancha;
      var options = {
        method: "DELETE",
      };
      fetch(url, options)
        .then((res) => res.text()) // or res.json()
        .then((res) => {
          location.reload();
        });
    },
    grabar() {
      let cancha = {
        nombre: this.nombre,
        precio: this.precio,
        tipo: this.tipo,
        imagen: this.imagen,
      };
      var options = {
        body: JSON.stringify(cancha),
        method: "POST",
        headers: { "Content-Type": "application/json" },
        redirect: "follow",
      };

      fetch(this.url, options)
        .then(() => {
          alert("Cancha agregada exitosamente");
          window.location.href = "./canchas.html";
        })
        .catch((err) => {
          console.error(err);
          alert("Error al agregar cancha");
        });
    },
  },
  created() {
    this.fetchData(this.url);
  },
}).mount("#app");
