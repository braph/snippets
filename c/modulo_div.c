
uint16_t                iter;

int iterState(struct scan_state_t *st) {
   int n_iter = num_ports * num_auths;

   st->iter++;
   if (st->iter > n_iter)
      return 0;

   st->server.sin_port =  ports[ st->iter / num_ports  ];
   st->auth            = &(AUTH[ st-> iter % num_auths ]);
   return 1;
}
