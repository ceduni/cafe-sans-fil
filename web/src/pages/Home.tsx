import React, { useEffect, useRef, useState, useMemo } from 'react';
import * as d3 from 'd3';
import styled from 'styled-components';
import type { Days, TimeBlock } from '../models/Cafe';
import type { CafeNode, EventNode } from '../models/Node';
import { generateMockData } from "../data/CafeMockData"
import { FACULTY_COLORS } from '@utils/Colors';

export type Feature = string;

// Styled Components
const Container = styled.div`
  width: 100vw;
  height: 100vh;
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
`;

const Controls = styled.div`
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const SearchInput = styled.input`
  padding: 12px 20px;
  border-radius: 25px;
  border: none;
  font-size: 16px;
  width: 350px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  
  &:focus {
    outline: none;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  }
`;

const ZoomButton = styled.button<{ active: boolean }>`
  padding: 12px 24px;
  border-radius: 25px;
  border: none;
  background: ${props => props.active ? '#667eea' : 'white'};
  color: ${props => props.active ? 'white' : '#4a5568'};
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  }
`;

// Filter Panel Styles
const FilterPanel = styled.div<{ show: boolean }>`
  position: fixed;
  top: 0;
  left: ${props => props.show ? '0' : '-400px'};
  width: 400px;
  height: 100vh;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
  z-index: 100;
  transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-y: auto;
  padding: 20px;

  @media (max-width: 768px) {
    width: 100%;
    left: ${props => props.show ? '0' : '-100%'};
  }
`;

const FilterToggle = styled.button`
  position: fixed;
  top: 20px;
  left: 390px;
  z-index: 101;
  padding: 12px 20px;
  border-radius: 0 25px 25px 0;
  border: none;
  background: white;
  color: #4a5568;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s;

  &:hover {
    transform: translateX(5px);
  }
`;

const FilterSection = styled.div`
  margin-bottom: 25px;
`;

const FilterTitle = styled.h3`
  margin: 0 0 12px 0;
  color: #2d3748;
  font-size: 1em;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const FilterCheckbox = styled.label`
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 8px 0;
  cursor: pointer;
  color: #4a5568;
  font-size: 0.95em;

  input {
    cursor: pointer;
  }
`;

const FilterRange = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const RangeInput = styled.input`
  width: 100%;
  cursor: pointer;
`;

const RangeLabel = styled.div`
  display: flex;
  justify-content: space-between;
  color: #718096;
  font-size: 0.85em;
`;

const ClearButton = styled.button`
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  border: none;
  background: #667eea;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: #5568d3;
    transform: translateY(-1px);
  }
`;

// Hover Preview Styles
const HoverPreview = styled.div<{ x: number; y: number; show: boolean }>`
  position: fixed;
  left: ${props => props.x}px;
  top: ${props => props.y}px;
  background: white;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  pointer-events: none;
  z-index: 999;
  min-width: 250px;
  max-width: 300px;
  opacity: ${props => props.show ? 1 : 0};
  transform: ${props => props.show ? 'scale(1)' : 'scale(0.95)'};
  transition: opacity 0.2s ease, transform 0.2s ease;
`;

const PreviewTitle = styled.h4`
  margin: 0 0 8px 0;
  color: #2d3748;
  font-size: 1.1em;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const PreviewStatus = styled.span<{ isOpen: boolean }>`
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${props => props.isOpen ? '#10b981' : '#ef4444'};
`;

const PreviewContent = styled.div`
  color: #4a5568;
  font-size: 0.9em;
  line-height: 1.5;
`;

const PreviewItem = styled.div`
  margin: 6px 0;
  display: flex;
  align-items: start;
  gap: 6px;
`;

const PreviewLabel = styled.span`
  font-weight: 600;
  color: #2d3748;
  min-width: 70px;
`;

// Event Time Label
const EventTimeLabel = styled.text`
  font-size: 10px;
  fill: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  pointer-events: none;
`;

const Legend = styled.div`
  position: absolute;
  bottom: 20px;
  left: 20px;
  background: rgba(255, 255, 255, 0.95);
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  max-width: 250px;
`;

const LegendTitle = styled.h4`
  margin: 0 0 10px 0;
  color: #2d3748;
  font-size: 14px;
`;

const LegendItem = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 5px 0;
  font-size: 12px;
  color: #4a5568;
`;

const ColorDot = styled.div<{ color: string }>`
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: ${props => props.color};
  flex-shrink: 0;
`;

// Sliding Panel
const SlidingPanel = styled.div<{ show: boolean }>`
  position: fixed;
  top: 0;
  right: ${props => props.show ? '0' : '-500px'};
  width: 500px;
  height: 100vh;
  background: white;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.3);
  z-index: 1001;
  transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-y: auto;

  @media (max-width: 768px) {
    width: 100%;
    right: ${props => props.show ? '0' : '-100%'};
  }
`;

const PanelOverlay = styled.div<{ show: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
  z-index: 1000;
  opacity: ${props => props.show ? 1 : 0};
  pointer-events: ${props => props.show ? 'all' : 'none'};
  transition: opacity 0.4s ease;
`;

const PanelHeader = styled.div`
  position: sticky;
  top: 0;
  background: white;
  padding: 30px;
  border-bottom: 1px solid #e2e8f0;
  z-index: 10;
`;

const CloseButton = styled.button`
  position: absolute;
  top: 20px;
  right: 20px;
  background: #f7fafc;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 24px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: #4a5568;

  &:hover {
    background: #e2e8f0;
    transform: rotate(90deg);
  }
`;

const PanelTitle = styled.h2`
  margin: 0 0 5px 0;
  color: #2d3748;
  font-size: 2em;
  padding-right: 50px;
`;

const PanelSubtitle = styled.div`
  color: #718096;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const StatusBadge = styled.span<{ isOpen: boolean }>`
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 12px;
  background: ${props => props.isOpen ? '#10b981' : '#ef4444'};
  color: white;
  font-size: 0.85em;
  font-weight: 600;

  &::before {
    content: '';
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: white;
  }
`;

const PanelContent = styled.div`
  padding: 30px;
`;

const Section = styled.div`
  margin-bottom: 30px;
`;

const SectionTitle = styled.h3`
  margin: 0 0 15px 0;
  color: #2d3748;
  font-size: 1.2em;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const InfoGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
`;

const InfoBox = styled.div`
  background: #f7fafc;
  padding: 15px;
  border-radius: 10px;
`;

const InfoLabel = styled.div`
  color: #718096;
  font-size: 0.85em;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 5px;
`;

const InfoValue = styled.div`
  color: #2d3748;
  font-size: 1.05em;
  word-break: break-word;
`;

const FeaturesList = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
`;

const FeatureTag = styled.span`
  padding: 6px 12px;
  background: #667eea;
  color: white;
  border-radius: 15px;
  font-size: 0.85em;
`;

const HoursTable = styled.div`
  background: #f7fafc;
  border-radius: 10px;
  overflow: hidden;
`;

const HoursRow = styled.div<{ isToday?: boolean }>`
  display: flex;
  justify-content: space-between;
  padding: 12px 15px;
  border-bottom: 1px solid #e2e8f0;
  background: ${props => props.isToday ? '#eef2ff' : 'transparent'};
  font-weight: ${props => props.isToday ? '600' : '400'};
  
  &:last-child {
    border-bottom: none;
  }
`;

const PaymentMethodBadge = styled.span`
  padding: 4px 10px;
  background: #e2e8f0;
  border-radius: 8px;
  font-size: 0.85em;
  color: #4a5568;
  margin-right: 6px;
`;

const ContactLink = styled.a`
  color: #667eea;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 8px 0;
  
  &:hover {
    text-decoration: underline;
  }
`;

const HealthScore = styled.div<{ score: number }>`
  width: 100%;
  height: 12px;
  background: #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
  margin-top: 10px;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: ${props => props.score}%;
    background: ${props =>
        props.score >= 90 ? 'linear-gradient(90deg, #10b981, #34d399)' :
            props.score >= 70 ? 'linear-gradient(90deg, #3b82f6, #60a5fa)' :
                props.score >= 50 ? 'linear-gradient(90deg, #f59e0b, #fbbf24)' :
                    'linear-gradient(90deg, #ef4444, #f87171)'
    };
    border-radius: 10px;
    transition: width 0.5s ease;
  }
`;

// Filter state interface
interface FilterState {
    faculties: Set<string>;
    statuses: Set<'open' | 'closed'>;
    features: Set<string>;
    paymentMethods: Set<string>;
    healthScoreMin: number;
    activityLevelMin: number;
    activityLevelMax: number;
}

// Helper function to format relative time
const getRelativeTime = (timestamp: Date): string => {
    const now = new Date();
    const diffMs = timestamp.getTime() - now.getTime();
    const diffMinutes = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMinutes / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMinutes < 0) return 'Started';
    if (diffMinutes < 60) return `in ${diffMinutes}m`;
    if (diffHours < 24) return `in ${diffHours}h`;
    if (diffDays < 7) return `in ${diffDays}d`;
    return `in ${Math.floor(diffDays / 7)}w`;
};

const BouncingCafes: React.FC = () => {
    const svgRef = useRef<SVGSVGElement>(null);
    const [dimensions, setDimensions] = useState({
        width: window.innerWidth,
        height: window.innerHeight
    });
    const [cafes, setCafes] = useState<CafeNode[]>([]);
    const [events, setEvents] = useState<EventNode[]>([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCafe, setSelectedCafe] = useState<CafeNode | null>(null);
    // const [pausedCafeIds, setPausedCafeIds] = useState<Set<string>>(new Set());
    const [hoveredCafe, setHoveredCafe] = useState<CafeNode | null>(null);
    const [hoverPosition, setHoverPosition] = useState({ x: 0, y: 0 });
    const [zoomedOut, setZoomedOut] = useState(false);
    const [showFilters, setShowFilters] = useState(false);
    const [useCoordinates, setUseCoordinates] = useState(false);
    const [loading, setLoading] = useState(true);
    const simulationRef = useRef<d3.Simulation<CafeNode, undefined> | null>(null);
    const animationFrameRef = useRef<number | null>(null);
    const selectedCafeRef = useRef<CafeNode | null>(null);
    const setSelectedCafeRef = useRef<(cafe: CafeNode | null) => void>(() => { });

    // Filter state
    const [filters, setFilters] = useState<FilterState>({
        faculties: new Set<string>(),
        statuses: new Set<'open' | 'closed'>(),
        features: new Set<string>(),
        paymentMethods: new Set<string>(),
        healthScoreMin: 0,
        activityLevelMin: 0,
        activityLevelMax: 100
    });

    // Keep refs in sync
    useEffect(() => {
        selectedCafeRef.current = selectedCafe;
    }, [selectedCafe]);

    useEffect(() => {
        setSelectedCafeRef.current = setSelectedCafe;
    }, []);

    // Generate mock cafes with coordinates
    useEffect(() => {
        const mockCafes: CafeNode[] = generateMockData(dimensions);

        // Add mock coordinates for positioning (simulating campus layout)
        const enhancedCafes = mockCafes.map((cafe, idx) => {
            // Generate coordinates based on faculty (simulating building clusters)
            const facultyIndex = Array.from(new Set(mockCafes.map(c => c.affiliation.faculty)))
                .indexOf(cafe.affiliation.faculty);
            const angle = (facultyIndex / 8) * 2 * Math.PI;
            const baseRadius = 0.3;
            const jitter = (Math.random() - 0.5) * 0.1;

            return {
                ...cafe,
                coordinates: {
                    lat: 45.5 + Math.cos(angle) * (baseRadius + jitter),
                    lng: -73.6 + Math.sin(angle) * (baseRadius + jitter)
                },
                logo: `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(cafe.name)}&backgroundColor=667eea`
            };
        });

        setCafes(enhancedCafes);

        // Generate events with timestamps
        const now = new Date();
        const mockEvents: EventNode[] = enhancedCafes.flatMap(cafe => {
            const numEvents = Math.floor(Math.random() * 4);
            return Array.from({ length: numEvents }, (_, i) => {
                const hoursFromNow = Math.random() * 168; // Random time within next week
                const eventTime = new Date(now.getTime() + hoursFromNow * 60 * 60 * 1000);

                return {
                    id: `event-${cafe.id}-${i}`,
                    cafeId: cafe.id,
                    title: ['Study Group', 'Workshop', 'Networking', 'Open Mic', 'Game Night'][Math.floor(Math.random() * 5)],
                    time: eventTime.toISOString(),
                    timestamp: eventTime,
                    attendance: Math.floor(Math.random() * 100) + 10, // 10-110 people
                    color: ['#3b82f6', '#10b981', '#f59e0b', '#ec4899'][Math.floor(Math.random() * 4)],
                    angle: Math.random() * Math.PI * 2
                };
            });
        });

        setEvents(mockEvents);
        setLoading(false);
    }, [dimensions.width, dimensions.height]);


    const filteredCafes = useMemo(() => {
        return cafes.filter(cafe => {
            const matchesSearch =
                cafe.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                cafe.affiliation.faculty.toLowerCase().includes(searchTerm.toLowerCase()) ||
                cafe.location.pavillon.toLowerCase().includes(searchTerm.toLowerCase());

            if (!matchesSearch) return false;

            if (filters.faculties.size > 0 && !filters.faculties.has(cafe.affiliation.faculty)) {
                return false;
            }

            if (filters.statuses.size > 0) {
                const status = cafe.is_open ? 'open' : 'closed';
                if (!filters.statuses.has(status)) return false;
            }

            if (filters.features.size > 0) {
                const hasFeature = Array.from(filters.features).some(feature =>
                    cafe.features.includes(feature)
                );
                if (!hasFeature) return false;
            }

            if (filters.paymentMethods.size > 0) {
                const hasPayment = Array.from(filters.paymentMethods).some(method =>
                    cafe.payment_details.some(p => p.method === method)
                );
                if (!hasPayment) return false;
            }

            if (cafe.health_score < filters.healthScoreMin) return false;

            if (
                cafe.activityLevel < filters.activityLevelMin ||
                cafe.activityLevel > filters.activityLevelMax
            ) {
                return false;
            }

            return true;
        });
    }, [cafes, searchTerm, filters]);


    // Get all unique values for filter options
    const uniqueFaculties = useMemo(
        () => Array.from(new Set(cafes.map(c => c.affiliation.faculty))),
        [cafes]
    );

    const uniqueFeatures = Array.from(new Set(cafes.flatMap(c => c.features)));
    const uniquePaymentMethods = Array.from(
        new Set(cafes.flatMap(c => c.payment_details.map(p => p.method)))
    );

    // Handle resize
    useEffect(() => {
        const handleResize = () => {
            setDimensions({ width: window.innerWidth, height: window.innerHeight });
        };
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    // D3 Visualization
    useEffect(() => {
        if (!svgRef.current || filteredCafes.length === 0) return;

        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove();

        if (zoomedOut) {
            renderDepartmentView(svg);
        } else {
            renderCafeView(svg);
        }

        return () => {
            if (simulationRef.current) {
                simulationRef.current.stop();
            }
            if (animationFrameRef.current) {
                cancelAnimationFrame(animationFrameRef.current);
            }
        };
    }, [filteredCafes, dimensions, zoomedOut, selectedCafe, useCoordinates]);

    const renderDepartmentView = (svg: d3.Selection<SVGSVGElement, unknown, null, undefined>) => {
        const departments: { [key: string]: CafeNode[] } = {};
        filteredCafes.forEach(cafe => {
            const faculty = cafe.location.pavillon;
            if (!departments[faculty]) {
                departments[faculty] = [];
            }
            departments[faculty].push(cafe);
        });

        const departmentList = Object.keys(departments);
        const departmentCenters: { [key: string]: { x: number; y: number } } = {};

        departmentList.forEach((dept, i) => {
            const angle = (i / departmentList.length) * 2 * Math.PI;
            const radiusX = dimensions.width * 0.3; // Horizontal radius
            const radiusY = dimensions.height * 0.25; // Vertical radius (smaller for horizontal spread)
            departmentCenters[dept] = {
                x: dimensions.width / 2 + Math.cos(angle) * radiusX,
                y: dimensions.height / 2 + Math.sin(angle) * radiusY
            };
        });

        const deptGroups = svg.selectAll('g.department')
            .data(departmentList)
            .join('g')
            .attr('class', 'department')
            .attr('transform', d => {
                const center = departmentCenters[d];
                return `translate(${center.x},${center.y})`;
            })
            .style('cursor', 'pointer')
            .on('click', () => setZoomedOut(false));

        deptGroups.append('circle')
            .attr('r', 100)
            .attr('fill', d => FACULTY_COLORS[d] || FACULTY_COLORS['default'])
            .attr('opacity', 0.3)
            .style('filter', 'drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3))');

        deptGroups.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', '-10')
            .style('font-size', '24px')
            .style('font-weight', 'bold')
            .style('fill', 'white')
            .style('text-shadow', '2px 2px 4px rgba(0, 0, 0, 0.8)')
            .style('pointer-events', 'none')
            .text(d => d);

        deptGroups.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', '15')
            .style('font-size', '16px')
            .style('fill', 'white')
            .style('opacity', 0.9)
            .style('text-shadow', '1px 1px 3px rgba(0, 0, 0, 0.8)')
            .style('pointer-events', 'none')
            .text(d => `${departments[d].length} ${departments[d].length === 1 ? 'Café' : 'Cafés'}`);
    };

    const coordsToScreen = (lat: number, lng: number) => {
        // Simple mercator-like projection
        const latRange = [45.3, 45.7];
        const lngRange = [-73.8, -73.4];

        const x = ((lng - lngRange[0]) / (lngRange[1] - lngRange[0])) * dimensions.width * 0.8 + dimensions.width * 0.1;
        const y = ((lat - latRange[0]) / (latRange[1] - latRange[0])) * dimensions.height * 0.8 + dimensions.height * 0.1;

        return { x, y };
    };

    const renderCafeView = (svg: d3.Selection<SVGSVGElement, unknown, null, undefined>) => {
        const faculties = Array.from(new Set(filteredCafes.map(c => c.affiliation.faculty)));
        const departmentCenters: { [key: string]: { x: number; y: number } } = {};

        if (!useCoordinates) {
            // Original faculty-based positioning
            faculties.forEach((faculty, i) => {
                const angle = (i / faculties.length) * 2 * Math.PI;
                const radiusX = dimensions.width * 0.3; // Horizontal radius
                const radiusY = dimensions.height * 0.25; // Vertical radius (smaller)
                // const radius = Math.min(dimensions.width, dimensions.height) * 0.25;
                departmentCenters[faculty] = {
                    x: dimensions.width / 2 + Math.cos(angle) * radiusX,
                    y: dimensions.height / 2 + Math.sin(angle) * radiusY
                };
            });

            const deptGroup = svg.append('g');
            faculties.forEach(faculty => {
                const center = departmentCenters[faculty];
                deptGroup.append('circle')
                    .attr('cx', center.x)
                    .attr('cy', center.y)
                    .attr('r', 150)
                    .attr('fill', FACULTY_COLORS[faculty] || FACULTY_COLORS['default'])
                    .attr('opacity', 0.15);

                deptGroup.append('circle')
                    .attr('cx', center.x)
                    .attr('cy', center.y)
                    .attr('r', 150)
                    .attr('fill', 'none')
                    .attr('stroke', FACULTY_COLORS[faculty] || FACULTY_COLORS['default'])
                    .attr('stroke-width', 2)
                    .attr('stroke-dasharray', '5,5')
                    .attr('opacity', 0.5);

                deptGroup.append('text')
                    .attr('x', center.x)
                    .attr('y', center.y - 160)
                    .attr('text-anchor', 'middle')
                    .attr('fill', 'white')
                    .attr('font-weight', 'bold')
                    .style('text-shadow', '2px 2px 4px rgba(0, 0, 0, 0.5)')
                    .text(faculty);
            });
        }

        // Initialize positions based on coordinates or faculties
        filteredCafes.forEach(cafe => {
            if (useCoordinates && cafe.coordinates) {
                const screen = coordsToScreen(cafe.coordinates.lat, cafe.coordinates.lng);
                cafe.x = screen.x;
                cafe.y = screen.y;
            } else if (!cafe.x || !cafe.y) {
                const center = departmentCenters[cafe.affiliation.faculty] ||
                    { x: dimensions.width / 2, y: dimensions.height / 2 };
                cafe.x = center.x + (Math.random() - 0.5) * 250;
                cafe.y = center.y + (Math.random() - 0.5) * 150;
            }
        });

        const simulation = d3.forceSimulation(filteredCafes)
            .force('charge', d3.forceManyBody().strength(useCoordinates ? 10 : 30))
            .force('collision', d3.forceCollide<CafeNode>(d => {
                const currentSelected = selectedCafeRef.current;
                return d.id === currentSelected?.id ? d.radius * 2 + 20 : d.radius + 20;
            }))
            .force('x', d3.forceX((d: CafeNode) => {
                if (useCoordinates && d.coordinates) {
                    return coordsToScreen(d.coordinates.lat, d.coordinates.lng).x;
                }
                return departmentCenters[d.affiliation.faculty]?.x || dimensions.width / 2;
            }).strength(useCoordinates ? 0.8 : 0.05))
            .force('y', d3.forceY((d: CafeNode) => {
                if (useCoordinates && d.coordinates) {
                    return coordsToScreen(d.coordinates.lat, d.coordinates.lng).y;
                }
                return departmentCenters[d.affiliation.faculty]?.y || dimensions.height / 2;
            }).strength(useCoordinates ? 0.8 : 0.05))
            .velocityDecay(0.3);

        simulationRef.current = simulation;

        const cafeGroups = svg.selectAll<SVGGElement, CafeNode>('g.cafe')
            .data(filteredCafes, d => d.id)
            .join('g')
            .attr('class', 'cafe')
            .style('cursor', 'pointer')
            .call(d3.drag<SVGGElement, CafeNode>()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));

        cafeGroups.each(function (d) {
            if (d.activityLevel > 30 && d.is_open) {
                const color = d.activityLevel > 70 ? '#ef4444' : d.activityLevel > 50 ? '#f59e0b' : '#10b981';
                const speed = 2500 - (d.activityLevel / 100) * 1500;

                const ring = d3.select(this).append('circle')
                    .attr('r', d.radius + 5)
                    .attr('fill', 'none')
                    .attr('stroke', color)
                    .attr('stroke-width', 3)
                    .attr('opacity', 0.8)
                    .style('pointer-events', 'none');

                function pulse() {
                    ring.transition().duration(speed / 2)
                        .attr('r', d.radius + 20)
                        .attr('opacity', 0)
                        .transition().duration(0)
                        .attr('r', d.radius + 5)
                        .attr('opacity', 0.8)
                        .on('end', pulse);
                }
                pulse();
            }
        });

        cafeGroups.append('circle')
            .attr('class', 'main-circle')
            .attr('r', d => d.id === selectedCafe?.id ? d.radius * 1.8 : d.radius)
            .attr('fill', d => d.color)
            .style('filter', d =>
                d.id === selectedCafe?.id
                    ? 'drop-shadow(0 8px 20px rgba(0, 0, 0, 0.5))'
                    : 'drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3))'
            )
            .style('opacity', d => d.is_open ? 1 : 0.3)
            .transition()
            .duration(300)
            .attr('r', d => d.id === selectedCafe?.id ? d.radius * 1.8 : d.radius);

        // Add logo image (clipPath for circular mask)
        cafeGroups.append('defs')
            .append('clipPath')
            .attr('id', d => `clip-${d.id}`)
            .append('circle')
            .attr('r', d => d.id === selectedCafe?.id ? d.radius * 1.6 : d.radius * 0.9);

        cafeGroups.append('image')
            .attr('class', 'cafe-logo')
            .attr('href', d => d.logo || d.color)
            .attr('x', d => -(d.id === selectedCafe?.id ? d.radius * 1.6 : d.radius * 0.9))
            .attr('y', d => -(d.id === selectedCafe?.id ? d.radius * 1.6 : d.radius * 0.9))
            .attr('width', d => (d.id === selectedCafe?.id ? d.radius * 3.2 : d.radius * 1.8))
            .attr('height', d => (d.id === selectedCafe?.id ? d.radius * 3.2 : d.radius * 1.8))
            .attr('clip-path', d => `url(#clip-${d.id})`)
            .style('opacity', d => d.is_open ? 1 : 0.3)
            .style('pointer-events', 'none');

        cafeGroups.append('circle')
            .attr('r', 8)
            .attr('cx', d => (d.id === selectedCafe?.id ? d.radius * 1.8 : d.radius) - 12)
            .attr('cy', d => -(d.id === selectedCafe?.id ? d.radius * 1.8 : d.radius) + 12)
            .attr('fill', d => d.is_open ? '#10b981' : '#ef4444')
            .attr('stroke', 'white')
            .attr('stroke-width', 2)
            .style('pointer-events', 'none');

        cafeGroups.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', d => (d.id === selectedCafe?.id ? d.radius * 1.8 : d.radius) + 20)
            .style('font-weight', '600')
            .style('font-size', d => d.id === selectedCafe?.id ? '16px' : '14px')
            .style('fill', 'white')
            .style('pointer-events', 'none')
            .style('text-shadow', '2px 2px 4px rgba(0, 0, 0, 0.8)')
            .style('opacity', d => d.is_open ? 1 : 0.5)
            .text(d => d.name);

        cafeGroups.on('click', function (event, d) {
            event.stopPropagation();
            setHoveredCafe(null);
            const currentSelected = selectedCafeRef.current;
            setSelectedCafeRef.current(currentSelected?.id === d.id ? null : d);
        });

        cafeGroups.on('mouseenter', function (event, d) {
            const currentSelected = selectedCafeRef.current;
            if (!currentSelected) {
                const [x, y] = d3.pointer(event, document.body);
                setHoveredCafe(d);
                setHoverPosition({ x: x + 20, y: y - 10 });
            }

            if (d.id !== currentSelected?.id) {
                d3.select(this).select('.main-circle')
                    .transition().duration(200)
                    .attr('r', d.radius * 1.15);
                d3.select(this).select('.cafe-logo')
                    .transition().duration(200)
                    .attr('x', -d.radius * 1.15 * 0.9)
                    .attr('y', -d.radius * 1.15 * 0.9)
                    .attr('width', d.radius * 1.15 * 1.8)
                    .attr('height', d.radius * 1.15 * 1.8);
            }
        }).on('mousemove', function (event) {
            const currentSelected = selectedCafeRef.current;
            if (!currentSelected) {
                const [x, y] = d3.pointer(event, document.body);
                setHoverPosition({ x: x + 20, y: y - 10 });
            }
        }).on('mouseleave', function (event, d) {
            setHoveredCafe(null);
            const currentSelected = selectedCafeRef.current;
            if (d.id !== currentSelected?.id) {
                d3.select(this).select('.main-circle')
                    .transition().duration(200)
                    .attr('r', d.radius);
                d3.select(this).select('.cafe-logo')
                    .transition().duration(200)
                    .attr('x', -d.radius * 0.9)
                    .attr('y', -d.radius * 0.9)
                    .attr('width', d.radius * 1.8)
                    .attr('height', d.radius * 1.8);
            }
        });

        if (events.length > 0) {
            // Cancel any existing animation
            if (animationFrameRef.current) {
                cancelAnimationFrame(animationFrameRef.current);
            }

            const eventGroups = svg.selectAll<SVGGElement, EventNode>('g.event')
                .data(events.filter(e => filteredCafes.some(c => c.id === e.cafeId)))
                .join('g')
                .attr('class', 'event');

            // Calculate event radius based on attendance
            const getEventRadius = (attendance: number) => {
                return Math.max(8, Math.min(20, 8 + (attendance / 100) * 12));
            };

            // Calculate orbit radius based on time (sooner = closer)
            const getOrbitRadius = (timestamp: Date, parentRadius: number) => {
                const now = new Date();
                const hoursUntil = (timestamp.getTime() - now.getTime()) / (1000 * 60 * 60);
                const maxHours = 168; // 1 week
                const minOrbit = parentRadius + 25;
                const maxOrbit = parentRadius + 60;

                // Closer events orbit closer to the cafe
                const distanceFactor = Math.min(hoursUntil / maxHours, 1);
                return minOrbit + (maxOrbit - minOrbit) * distanceFactor;
            };

            eventGroups.append('circle')
                .attr('r', d => getEventRadius(d.attendance))
                .attr('fill', d => d.color)
                .attr('stroke', 'white')
                .attr('stroke-width', 2)
                .style('filter', 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4))');

            // Add time label next to event
            eventGroups.append('text')
                .attr('class', 'event-time')
                .attr('x', d => getEventRadius(d.attendance) + 8)
                .attr('y', 4)
                .style('font-size', '10px')
                .style('fill', 'white')
                .style('font-weight', '600')
                .style('text-shadow', '1px 1px 2px rgba(0, 0, 0, 0.8)')
                .style('pointer-events', 'none')
                .text(d => d.timestamp ? getRelativeTime(d.timestamp) : '');

            // Add enhanced tooltip with title element
            eventGroups.append('title')
                .text(d => {
                    const timeStr = d.timestamp ? getRelativeTime(d.timestamp) : d.time;
                    return `${d.title}\nStarts ${timeStr}\nExpected: ${d.attendance} attendees`;
                });

            const animate = () => {
                eventGroups.attr('transform', d => {
                    const parent = filteredCafes.find(c => c.id === d.cafeId);
                    if (!parent || !parent.x || !parent.y) return 'translate(0,0)';

                    d.angle = (d.angle || 0) + 0.01;
                    const currentSelected = selectedCafeRef.current;
                    const parentRadius = parent.id === currentSelected?.id ? parent.radius * 1.8 : parent.radius;
                    const orbitRadius = getOrbitRadius(d.timestamp, parentRadius);
                    const x = parent.x + Math.cos(d.angle) * orbitRadius;
                    const y = parent.y + Math.sin(d.angle) * orbitRadius;

                    return `translate(${x},${y})`;
                });
                animationFrameRef.current = requestAnimationFrame(animate);
            };
            animate();
        }

        simulation.on('tick', () => {
            filteredCafes.forEach(d => {
                const currentSelected = selectedCafeRef.current;
                const effectiveRadius = d.id === currentSelected?.id ? d.radius * 1.8 : d.radius;
                if (d.x! - effectiveRadius < 0 || d.x! + effectiveRadius > dimensions.width) {
                    d.vx = d.vx ? d.vx * -0.8 : 0;
                    d.x = Math.max(effectiveRadius, Math.min(dimensions.width - effectiveRadius, d.x!));
                }
                if (d.y! - effectiveRadius < 0 || d.y! + effectiveRadius > dimensions.height) {
                    d.vy = d.vy ? d.vy * -0.8 : 0;
                    d.y = Math.max(effectiveRadius, Math.min(dimensions.height - effectiveRadius, d.y!));
                }
            });

            cafeGroups.attr('transform', d => `translate(${d.x},${d.y})`);
        });

        function dragstarted(event: any) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event: any) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event: any) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }
    };

    const getTodayDay = (): Days => {
        const days: Days[] = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
        return days[new Date().getDay()];
    };

    const formatHours = (blocks: TimeBlock[]): string => {
        if (blocks.length === 0) return 'Closed';
        return blocks.map(b => `${b.start} - ${b.end}`).join(', ');
    };

    // Filter handlers
    const toggleFaculty = (faculty: string) => {
        setFilters(prev => {
            const newFaculties = new Set(prev.faculties);
            if (newFaculties.has(faculty)) {
                newFaculties.delete(faculty);
            } else {
                newFaculties.add(faculty);
            }
            return { ...prev, faculties: newFaculties };
        });
    };

    const toggleStatus = (status: 'open' | 'closed') => {
        setFilters(prev => {
            const newStatuses = new Set(prev.statuses);
            if (newStatuses.has(status)) {
                newStatuses.delete(status);
            } else {
                newStatuses.add(status);
            }
            return { ...prev, statuses: newStatuses };
        });
    };

    const toggleFeature = (feature: string) => {
        setFilters(prev => {
            const newFeatures = new Set(prev.features);
            if (newFeatures.has(feature)) {
                newFeatures.delete(feature);
            } else {
                newFeatures.add(feature);
            }
            return { ...prev, features: newFeatures };
        });
    };

    const togglePaymentMethod = (method: string) => {
        setFilters(prev => {
            const newMethods = new Set(prev.paymentMethods);
            if (newMethods.has(method)) {
                newMethods.delete(method);
            } else {
                newMethods.add(method);
            }
            return { ...prev, paymentMethods: newMethods };
        });
    };

    const clearFilters = () => {
        setFilters({
            faculties: new Set(),
            statuses: new Set(),
            features: new Set(),
            paymentMethods: new Set(),
            healthScoreMin: 0,
            activityLevelMin: 0,
            activityLevelMax: 100
        });
    };

    if (loading) {
        return (
            <Container>
                <div style={{ color: 'white', textAlign: 'center', paddingTop: '50vh' }}>Loading cafés...</div>
            </Container>
        );
    }

    return (
        <Container>
            <FilterToggle onClick={() => setShowFilters(!showFilters)}>
                {showFilters ? '✕ Close' : '☰ Filters'}
            </FilterToggle>

            <FilterPanel show={showFilters}>
                <h2 style={{ marginTop: 0, color: '#2d3748' }}>Filters</h2>

                <FilterSection>
                    <FilterTitle>Faculties</FilterTitle>
                    {uniqueFaculties.map(faculty => (
                        <FilterCheckbox key={faculty}>
                            <input
                                type="checkbox"
                                checked={filters.faculties.has(faculty)}
                                onChange={() => toggleFaculty(faculty)}
                            />
                            <ColorDot color={FACULTY_COLORS[faculty] || FACULTY_COLORS['default']} />
                            {faculty}
                        </FilterCheckbox>
                    ))}
                </FilterSection>

                <FilterSection>
                    <FilterTitle>Status</FilterTitle>
                    <FilterCheckbox>
                        <input
                            type="checkbox"
                            checked={filters.statuses.has('open')}
                            onChange={() => toggleStatus('open')}
                        />
                        <ColorDot color="#10b981" />
                        Open Now
                    </FilterCheckbox>
                    <FilterCheckbox>
                        <input
                            type="checkbox"
                            checked={filters.statuses.has('closed')}
                            onChange={() => toggleStatus('closed')}
                        />
                        <ColorDot color="#ef4444" />
                        Closed
                    </FilterCheckbox>
                </FilterSection>

                <FilterSection>
                    <FilterTitle>Features</FilterTitle>
                    {uniqueFeatures.map(feature => (
                        <FilterCheckbox key={feature}>
                            <input
                                type="checkbox"
                                checked={filters.features.has(feature)}
                                onChange={() => toggleFeature(feature)}
                            />
                            {feature}
                        </FilterCheckbox>
                    ))}
                </FilterSection>

                <FilterSection>
                    <FilterTitle>Payment Methods</FilterTitle>
                    {uniquePaymentMethods.map(method => (
                        <FilterCheckbox key={method}>
                            <input
                                type="checkbox"
                                checked={filters.paymentMethods.has(method)}
                                onChange={() => togglePaymentMethod(method)}
                            />
                            {method}
                        </FilterCheckbox>
                    ))}
                </FilterSection>

                <FilterSection>
                    <FilterTitle>Health Score</FilterTitle>
                    <FilterRange>
                        <RangeLabel>
                            <span>Minimum</span>
                            <span>{filters.healthScoreMin}%</span>
                        </RangeLabel>
                        <RangeInput
                            type="range"
                            min="0"
                            max="100"
                            value={filters.healthScoreMin}
                            onChange={(e) => setFilters(prev => ({
                                ...prev,
                                healthScoreMin: parseInt(e.target.value)
                            }))}
                        />
                    </FilterRange>
                </FilterSection>

                <FilterSection>
                    <FilterTitle>Activity Level</FilterTitle>
                    <FilterRange>
                        <RangeLabel>
                            <span>Min: {filters.activityLevelMin}%</span>
                            <span>Max: {filters.activityLevelMax}%</span>
                        </RangeLabel>
                        <RangeInput
                            type="range"
                            min="0"
                            max="100"
                            value={filters.activityLevelMin}
                            onChange={(e) => setFilters(prev => ({
                                ...prev,
                                activityLevelMin: parseInt(e.target.value)
                            }))}
                        />
                        <RangeInput
                            type="range"
                            min="0"
                            max="100"
                            value={filters.activityLevelMax}
                            onChange={(e) => setFilters(prev => ({
                                ...prev,
                                activityLevelMax: parseInt(e.target.value)
                            }))}
                        />
                    </FilterRange>
                </FilterSection>

                <FilterSection>
                    <FilterCheckbox>
                        <input
                            type="checkbox"
                            checked={useCoordinates}
                            onChange={() => setUseCoordinates(!useCoordinates)}
                        />
                        Use Geographic Layout
                    </FilterCheckbox>
                </FilterSection>

                <ClearButton onClick={clearFilters}>
                    Clear All Filters
                </ClearButton>
            </FilterPanel>

            <Controls style={{ left: showFilters ? '420px' : '20px', transition: 'left 0.4s' }}>
                <SearchInput
                    type="text"
                    placeholder="Search cafés, faculties, or locations..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <ZoomButton active={zoomedOut} onClick={() => setZoomedOut(!zoomedOut)}>
                    {zoomedOut ? '🔍 Show Cafés' : '🗺️ Show Departments'}
                </ZoomButton>
            </Controls>

            <svg ref={svgRef} width={dimensions.width} height={dimensions.height} />

            {/* Hover Preview */}
            <HoverPreview x={hoverPosition.x} y={hoverPosition.y} show={!!hoveredCafe && !selectedCafe}>
                {hoveredCafe && (
                    <>
                        <PreviewTitle>
                            <PreviewStatus isOpen={hoveredCafe.is_open} />
                            {hoveredCafe.name}
                        </PreviewTitle>
                        <PreviewContent>
                            <PreviewItem>
                                <PreviewLabel>Faculty:</PreviewLabel>
                                {hoveredCafe.affiliation.faculty}
                            </PreviewItem>
                            <PreviewItem>
                                <PreviewLabel>Location:</PreviewLabel>
                                {hoveredCafe.location.pavillon}, {hoveredCafe.location.local}
                            </PreviewItem>
                            <PreviewItem>
                                <PreviewLabel>Health:</PreviewLabel>
                                {hoveredCafe.health_score}%
                            </PreviewItem>
                            {hoveredCafe.features.length > 0 && (
                                <PreviewItem style={{ flexDirection: 'column', alignItems: 'start' }}>
                                    <PreviewLabel>Features:</PreviewLabel>
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '4px' }}>
                                        {hoveredCafe.features.slice(0, 3).map(f => (
                                            <span key={f} style={{
                                                fontSize: '0.75em',
                                                padding: '2px 8px',
                                                background: '#667eea',
                                                color: 'white',
                                                borderRadius: '10px'
                                            }}>
                                                {f}
                                            </span>
                                        ))}
                                        {hoveredCafe.features.length > 3 && (
                                            <span style={{ fontSize: '0.75em', color: '#718096' }}>
                                                +{hoveredCafe.features.length - 3} more
                                            </span>
                                        )}
                                    </div>
                                </PreviewItem>
                            )}
                        </PreviewContent>
                    </>
                )}
            </HoverPreview>

            {!zoomedOut && (
                <Legend>
                    <LegendTitle>Viewing {filteredCafes.length} of {cafes.length} cafés</LegendTitle>
                    <div style={{ margin: '10px 0', borderTop: '1px solid #e2e8f0' }}></div>
                    <LegendTitle>Status</LegendTitle>
                    <LegendItem>
                        <ColorDot color="#10b981" />
                        <span>Open</span>
                    </LegendItem>
                    <LegendItem>
                        <ColorDot color="#ef4444" />
                        <span>Closed (Dimmed)</span>
                    </LegendItem>
                </Legend>
            )}

            <PanelOverlay show={!!selectedCafe} onClick={() => setSelectedCafe(null)} />
            <SlidingPanel show={!!selectedCafe}>
                {selectedCafe && (
                    <>
                        <PanelHeader>
                            <CloseButton onClick={() => setSelectedCafe(null)}>×</CloseButton>
                            <PanelTitle>{selectedCafe.name}</PanelTitle>
                            <PanelSubtitle>
                                <StatusBadge isOpen={selectedCafe.is_open}>
                                    {selectedCafe.is_open ? 'Open' : 'Closed'}
                                </StatusBadge>
                                {selectedCafe.affiliation.faculty}
                            </PanelSubtitle>
                        </PanelHeader>

                        <PanelContent>
                            {selectedCafe.description && (
                                <Section>
                                    <p style={{ color: '#4a5568', lineHeight: '1.6' }}>{selectedCafe.description}</p>
                                </Section>
                            )}

                            <InfoGrid>
                                <InfoBox>
                                    <InfoLabel>Location</InfoLabel>
                                    <InfoValue>
                                        {selectedCafe.location.pavillon}<br />
                                        {selectedCafe.location.local}
                                        {selectedCafe.location.floor && ` - Floor ${selectedCafe.location.floor}`}
                                    </InfoValue>
                                </InfoBox>
                                <InfoBox>
                                    <InfoLabel>Health Score</InfoLabel>
                                    <InfoValue>{selectedCafe.health_score}%</InfoValue>
                                    <HealthScore score={selectedCafe.health_score} />
                                </InfoBox>
                            </InfoGrid>

                            {selectedCafe.features.length > 0 && (
                                <Section>
                                    <SectionTitle>✨ Features</SectionTitle>
                                    <FeaturesList>
                                        {selectedCafe.features.map(feature => (
                                            <FeatureTag key={feature}>{feature}</FeatureTag>
                                        ))}
                                    </FeaturesList>
                                </Section>
                            )}

                            <Section>
                                <SectionTitle>🕐 Opening Hours</SectionTitle>
                                <HoursTable>
                                    {selectedCafe.opening_hours.map(dayHours => (
                                        <HoursRow key={dayHours.day} isToday={dayHours.day === getTodayDay()}>
                                            <span>{dayHours.day.charAt(0) + dayHours.day.slice(1).toLowerCase()}</span>
                                            <span>{formatHours(dayHours.blocks)}</span>
                                        </HoursRow>
                                    ))}
                                </HoursTable>
                            </Section>

                            {selectedCafe.payment_details.length > 0 && (
                                <Section>
                                    <SectionTitle>💳 Payment Methods</SectionTitle>
                                    <div>
                                        {selectedCafe.payment_details.map((payment, idx) => (
                                            <PaymentMethodBadge key={idx}>
                                                {payment.method}
                                                {payment.minimum && ` (min $${payment.minimum})`}
                                            </PaymentMethodBadge>
                                        ))}
                                    </div>
                                </Section>
                            )}

                            {(selectedCafe.contact.email || selectedCafe.contact.phone_number || selectedCafe.contact.website) && (
                                <Section>
                                    <SectionTitle>📞 Contact</SectionTitle>
                                    {selectedCafe.contact.email && (
                                        <ContactLink href={`mailto:${selectedCafe.contact.email}`}>
                                            ✉️ {selectedCafe.contact.email}
                                        </ContactLink>
                                    )}
                                    {selectedCafe.contact.phone_number && (
                                        <ContactLink href={`tel:${selectedCafe.contact.phone_number}`}>
                                            📱 {selectedCafe.contact.phone_number}
                                        </ContactLink>
                                    )}
                                    {selectedCafe.contact.website && (
                                        <ContactLink href={selectedCafe.contact.website} target="_blank" rel="noopener noreferrer">
                                            🌐 Visit Website
                                        </ContactLink>
                                    )}
                                </Section>
                            )}

                            {(selectedCafe.social_media.instagram || selectedCafe.social_media.facebook || selectedCafe.social_media.x) && (
                                <Section>
                                    <SectionTitle>📱 Social Media</SectionTitle>
                                    {selectedCafe.social_media.instagram && (
                                        <ContactLink href={`https://instagram.com/${selectedCafe.social_media.instagram.replace('@', '')}`} target="_blank">
                                            Instagram {selectedCafe.social_media.instagram}
                                        </ContactLink>
                                    )}
                                    {selectedCafe.social_media.facebook && (
                                        <ContactLink href={`https://facebook.com${selectedCafe.social_media.facebook}`} target="_blank">
                                            Facebook
                                        </ContactLink>
                                    )}
                                    {selectedCafe.social_media.x && (
                                        <ContactLink href={`https://x.com/${selectedCafe.social_media.x.replace('@', '')}`} target="_blank">
                                            X/Twitter {selectedCafe.social_media.x}
                                        </ContactLink>
                                    )}
                                </Section>
                            )}

                            {events.filter(e => e.cafeId === selectedCafe.id).length > 0 && (
                                <Section>
                                    <SectionTitle>🎉 Upcoming Events</SectionTitle>
                                    {events.filter(e => e.cafeId === selectedCafe.id).map(event => (
                                        <div key={event.id} style={{
                                            padding: '12px',
                                            background: '#f7fafc',
                                            borderLeft: `4px solid ${event.color}`,
                                            borderRadius: '5px',
                                            marginBottom: '10px'
                                        }}>
                                            <strong style={{ display: 'block', color: '#2d3748', marginBottom: '4px' }}>
                                                {event.title}
                                            </strong>
                                            <span style={{ color: '#718096', fontSize: '0.9em', display: 'block' }}>
                                                Starts {event.timestamp ? getRelativeTime(event.timestamp) : event.time}
                                            </span>
                                            <span style={{ color: '#4a5568', fontSize: '0.85em', marginTop: '4px', display: 'block' }}>
                                                Expected: {event.attendance} attendees
                                            </span>
                                        </div>
                                    ))}
                                </Section>
                            )}
                        </PanelContent>
                    </>
                )}
            </SlidingPanel>
        </Container>
    );
};

export default BouncingCafes;