import { AvisoExemplo } from "../exemplo.jsx";

// Ecrã 12. Avisos curtos quando um pedido muda de estado (Sofia). Cada um escolhe o que recebe.
export default function Notificacoes() {
  return (
    <section>
      <h1>Notificações</h1>
      <AvisoExemplo />
      <ul>
        <li>O teu pedido "Exportação de relatórios em PDF" passou a Em análise.</li>
        <li>A Marta mencionou-te em "Ligação ao Slack".</li>
        <li>O pedido "Lista de pedidos mais rápida" foi aceite.</li>
      </ul>
      <fieldset>
        <legend>Quero receber</legend>
        <label><input type="checkbox" defaultChecked /> Mudanças de estado dos meus pedidos</label>
        <label><input type="checkbox" defaultChecked /> Menções</label>
        <label><input type="checkbox" /> Também por email</label>
      </fieldset>
    </section>
  );
}
