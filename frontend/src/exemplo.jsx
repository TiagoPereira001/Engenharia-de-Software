// Dados de exemplo dos ecrãs que ainda não falam com a API (ligam no Sprint 4).
// Os números são inventados para a demonstração; não são medições.

export function AvisoExemplo() {
  return <p className="nota">Versão inicial com dados de exemplo. Este ecrã liga à API no Sprint 4.</p>;
}

export const RELEASES = [
  { nome: "Release 1.1", data: "30/11", progresso: 70, emRisco: false, contrato: true },
  { nome: "Release 2.0", data: "15/01", progresso: 25, emRisco: true, contrato: false },
  { nome: "Release 2.1", data: "28/02", progresso: 0, emRisco: false, contrato: false },
];

export const EQUIPAS = [
  { nome: "Equipa A", capacidade: 30, novo: 12, manutencao: 6, bugs: 10, administrativo: 4 },
  { nome: "Equipa B", capacidade: 30, novo: 15, manutencao: 4, bugs: 3, administrativo: 2 },
  { nome: "Equipa C", capacidade: 20, novo: 6, manutencao: 2, bugs: 2, administrativo: 1 },
];
