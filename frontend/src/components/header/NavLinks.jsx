import { 
  Brain, 
  Droplets, 
  Sprout, 
  Bug, 
  BarChart3,
  Trophy,
  MessageCircle
} from 'lucide-react'
import NavItem from './NavItem'

const navItems = [
  {
    path: '/ai-plant-analysis',
    translationKey: 'header.nav.aiPlantAnalysis',
    icon: Brain,
    gradient: 'from-purple-500 to-pink-500'
  },
  {
    path: '/smart-water-optimization',
    translationKey: 'header.nav.smartWaterOptimization',
    icon: Droplets,
    gradient: 'from-blue-500 to-cyan-500'
  },
  {
    path: '/soil-health-detection',
    translationKey: 'header.nav.soilHealthDetection',
    icon: Sprout,
    gradient: 'from-green-500 to-emerald-500'
  },
  {
    path: '/fertilizer-pest-diagnosis',
    translationKey: 'header.nav.fertilizerPestDiagnosis',
    icon: Bug,
    gradient: 'from-orange-500 to-red-500'
  },
  {
    path: '/dashboard',
    translationKey: 'header.nav.dashboard',
    icon: BarChart3,
    gradient: 'from-indigo-500 to-purple-500'
  },
  {
    path: '/achievements',
    translationKey: 'header.nav.achievements',
    icon: Trophy,
    gradient: 'from-yellow-500 to-orange-500'
  },
  {
    path: '/chatbot',
    translationKey: 'header.nav.chatbot',
    icon: MessageCircle,
    gradient: 'from-green-500 to-teal-500'
  }
]

export default function NavLinks() {
  return (
    <nav className="hidden lg:flex items-center gap-6">
      {navItems.map((item, index) => (
        <NavItem key={item.path} item={item} index={index} />
      ))}
    </nav>
  )
}
